from django.db import models
from datetime import datetime

# Create your models here.


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


class CompanyContact(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='+')


class Item(models.Model):
    label = models.CharField(max_length=100, null=False)
    quantity = models.IntegerField(null=False)  # This represents the quantity held by the supplier or client
    unit_price = models.FloatField(null=False)  # Price per unit


class Order(models.Model):
    received_date = models.DateTimeField(default=datetime.now)
    scheduled_deliver_date = models.DateTimeField(null=True)
    delivered_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, null=False)
    comments = models.TextField(null=True)

    items = models.ManyToManyField(Item, through='OrderItem')
    client = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='client_order')
    supplier = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='supplier_order')


class OrderItem(models.Model):
    quantity = models.IntegerField(null=False)
    price = models.FloatField(null=False)
    comments = models.TextField(null=True)

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
