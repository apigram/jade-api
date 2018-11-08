from rest_framework import serializers
from jadeapi.models import User, Company, Order, Item, Contact


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('url', 'name', 'business_number')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('url', 'received_date', 'scheduled_deliver_date', 'delivered_date', 'status', 'comments')


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('url', 'label', 'quantity', 'unit_price')


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'role', 'phone', 'email', 'address')
