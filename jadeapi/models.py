from django.db import models

# Create your models here.


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=1000)  # This value is hashed/salted.

    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='+')


class CompanyContact(models.Model):
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='+')


class Company(models.Model):
    name = models.CharField(max_length=200)
    business_number = models.CharField(max_length=100)  # In Australia this would be the ABN.

    contact = models.ForeignKey(CompanyContact, on_delete=models.CASCADE)
    suppliers = models.ManyToManyField("self")


class Item(models.Model):
    label = models.CharField(max_length=100)
    quantity = models.IntegerField()  # This represents the quantity held by the supplier or client
    unit_price = models.FloatField()  # Price per unit


class Order(models.Model):
    received_date = models.DateTimeField()
    scheduled_deliver_date = models.DateTimeField()
    delivered_date = models.DateTimeField()
    status = models.CharField(max_length=100)
    comments = models.TextField()

    items = models.ManyToManyField(Item, through='OrderItem')
    client = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='client_order')
    supplier = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='supplier_order')


class OrderItem(models.Model):
    quantity = models.IntegerField()
    price = models.FloatField()
    comments = models.TextField()

    orders = models.ForeignKey(Order, on_delete=models.CASCADE)
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
