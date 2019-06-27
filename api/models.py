from django.db import models
from django.conf import settings
from datetime import datetime
import django_pandas.io as pio
import django_pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression


def impute_overflow_days(cols):
    delivered_date = cols[0]
    scheduled_delivery = cols[1]

    return delivered_date - scheduled_delivery


def impute_delivery_on_time(cols):
    delivered_date = cols[0]
    scheduled_delivery = cols[1]

    if delivered_date - scheduled_delivery > 0:
        # Order is late
        return 0
    else:
        # Order is either on time or early.
        return 1


class State(models.Model):
    label = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=300, null=True)

    previous_state = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='next_state')


class Contact(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    role = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=200, null=False)


class Company(models.Model):
    COMPANY_TYPES = (
        ('CLIENT', 'Client'),
        ('SUPPLIER', 'Supplier')
    )
    name = models.CharField(max_length=200, null=False)
    business_number = models.CharField(max_length=100, null=False)  # In Australia this would be the ABN.
    type = models.CharField(max_length=20, choices=COMPANY_TYPES, null=False)

    # For suppliers, this is average orders made to that supplier over a month.
    # For clients, this is average orders received from that client over a month.
    avg_monthly_orders = models.IntegerField(null=False, default=0)

    # This field needs only be set for companies of type SUPPLIER.
    # Indicates, as a percentage, how reliable the supplier is at dispatching deliveries on time.
    # This can be used as a factor of safety (FoS) to more accurately schedule deliveries.
    delivery_reliability = models.FloatField()

    # Project how late an order made on the current date is likely to be delivered.
    def project_delivery_overflow(self):
        # Update supplier reliability using the list of late orders
        supplier_orders = Order.objects.filter(supplier=self.pk).all()
        df = pio.read_frame(supplier_orders)

        df['overflow'] = df[['delivered_date', 'scheduled_delivery_date']].apply(impute_overflow_days, axis=1)

        x_train = df['received_date']
        y_train = df['overflow']  # The number of days before/past the scheduled delivery date that the order was delivered.
        model = LinearRegression()

        model.fit(x_train, y_train)
        x_pred = datetime.today()
        y_pred = model.predict(x_pred)
        return y_pred

    # Update the reliability of the supplier based on how many orders have been late this month
    def update_reliability(self):
        supplier_orders = Order.objects.filter(supplier=self.pk).all()
        df = pio.read_frame(supplier_orders)

        df['delivery_on_time'] = df[['delivered_date', 'scheduled_delivery_date']].apply(impute_delivery_on_time, axis=1)

        x_train = df['received_date']
        y_train = df['delivery_on_time']

        model = LogisticRegression()
        model.fit(x_train, y_train)

        x_pred = datetime.today()
        y_pred = model.predict(x_pred)

        return y_pred

    # Gets the monthly received orders from a specific client.
    # Suppliers can use this data to determine the average volume of orders they will likely receive from the client.
    def get_monthly_received_orders(self):
        monthly_orders = Order.objects.filter(client_id=self.pk, received_date__month=datetime.today().month)
        return monthly_orders

    def get_monthly_orders(self):
        monthly_orders = Order.objects.filter(supplier_id=self.pk, received_date__month=datetime.today().month)
        return monthly_orders


class ApiUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='+')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="+")


class CompanyContact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='contacts')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='+')


class Item(models.Model):
    # Label is not unique because the same item could be delivered by a different supplier for a different unit price.
    label = models.CharField(max_length=100, null=False)
    quantity = models.IntegerField(null=False)   # This represents the quantity held by the supplier or client
    unit_price = models.FloatField(null=False)   # Price per unit
    low_stock_threshold = models.IntegerField()  # Threshold for which JADE will show low stock warnings.

    supplier = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="supplier_items")

    # Determine a new low stock threshold
    def project_low_stock_threshold(self):
        item_orders = OrderItem.objects.filter(item=self.pk)
        df = pio.read_frame(item_orders)
        # Process dataframe, train a ML model and make a projection to assign to that item.
        # Assign the projection to the item

    # Get the projected sales for the given item for the current month using the figures from the previous month.
    def project_sales(self):
        item_orders = OrderItem.objects.filter(item=self.pk).all()
        df = pio.read_frame(item_orders)
        x_train = df['month']
        y_train = df['total_sales']
        model = LinearRegression()

        model.fit(x_train, y_train)

        x_pred = datetime.today().month
        y_pred = model.predict(x_pred)

        return y_pred

    # Gets a list of all orders for the specified item.
    # The ML algorithms will use this data to determine low stock thresholds for a given item.
    def get_item_orders(self):
        orders = OrderItem.objects.filter(item=self.pk).all()
        return orders


class Order(models.Model):
    received_date = models.DateTimeField(default=datetime.now)
    scheduled_deliver_date = models.DateTimeField(null=True)
    delivered_date = models.DateTimeField(null=True)
    comments = models.TextField(null=True)

    order_items = models.ManyToManyField(Item, through='OrderItem', related_name='order')
    client = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='client_orders')
    supplier = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='supplier_orders')
    status = models.ForeignKey(State, on_delete=models.CASCADE, related_name='order')


class OrderItem(models.Model):
    quantity = models.IntegerField(null=False)
    unit_price = models.FloatField(null=False)
    comments = models.TextField(null=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='orders')
