from django.db import models
from datetime import datetime
import django_pandas.io as pio
import django_pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


class Contact(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    role = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=200, null=False)


class User(models.Model):
    username = models.CharField(max_length=100, unique=True, null=False)
    email = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=1000, null=False)  # This value is hashed/salted.

    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='+')


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


class CompanyContact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='contacts')
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='+')


class Item(models.Model):
    # Label is not unique because the same item could be delivered by a different supplier for a different unit price.
    label = models.CharField(max_length=100, null=False)
    quantity = models.IntegerField(null=False)   # This represents the quantity held by the supplier or client
    unit_price = models.FloatField(null=False)   # Price per unit
    low_stock_threshold = models.IntegerField()  # Threshold for which JADE will show low stock warnings.

    supplier = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="supplier_items")

    # Gets a list of all items that are projected to run out of stock within two weeks.
    # The system will use this data to recommend items to be ordered to keep stock available.
    # The data should also include projected quantity requirements.
    @staticmethod
    def get_low_stock():
        items = Item.objects.filter(quantity__lt=models.F('low_stock_threshold'))
        for item in items:
            item_orders = OrderItem.get_item_orders(item.id)
            df = pio.read_frame(item_orders)
            # Process dataframe, train a ML model and make a projection for each item.
            # Assign the projection to the item
        return items


class Order(models.Model):
    received_date = models.DateTimeField(default=datetime.now)
    scheduled_deliver_date = models.DateTimeField(null=True)
    delivered_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, null=False)
    comments = models.TextField(null=True)

    items = models.ManyToManyField(Item, through='OrderItem')
    client = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='client_orders')
    supplier = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='supplier_orders')

    # Gets a lists of all orders that have not been delivered by the scheduled delivery date.
    # Clients can use this data to determine reliability of suppliers to meet demand in time.
    # Suppliers can use this data to determine weaknesses in their supply chain to a given client.
    @staticmethod
    def get_late_orders():
        late_orders = Order.objects.filter(delivered_date__gt=models.F('scheduled_delivery_date')).all()
        # Update supplier reliability using the list of late orders
        df = pio.read_frame(late_orders)
        x_train = df['received_date']
        y_train = df['delivered_on_time'] #  1 if the delivered date is greater than the scheduled delivery date, otherwise 0
        model = LinearRegression()
        model.train(x_train, y_train)
        x_pred = datetime.date
        y_pred = model.fit(x_pred)
        return late_orders

    # Gets the monthly received orders from a specific client.
    # Suppliers can use this data to determine the average volume of orders they will likely receive from the client.
    @staticmethod
    def get_monthly_received_orders(client_id):
        monthly_orders = Order.objects.filter(client_id=client_id, received_date__month=datetime.today().month)
        return monthly_orders

    # Gets the monthly orders to a specific supplier.
    # Clients can use this data to determine the average volume of orders they will likely dispatch to the supplier.
    @staticmethod
    def get_monthly_orders(supplier_id):
        monthly_orders = Order.objects.filter(supplier_id=supplier_id, received_date__month=datetime.today().month)
        return monthly_orders


class OrderItem(models.Model):
    quantity = models.IntegerField(null=False)
    unit_price = models.FloatField(null=False)
    comments = models.TextField(null=True)

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='orders')

    # Gets a list of all orders for the specified item.
    # The ML algorithms will use this data to determine low stock thresholds for a given item.
    @staticmethod
    def get_item_orders(item_id):
        orders = OrderItem.objects.filter(item_id=item_id).all()
        return orders

