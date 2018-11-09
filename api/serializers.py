from rest_framework import serializers
from api.models import User, Company, Order, Item, Contact, OrderItem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'contact', 'email')


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('url', 'name', 'contacts', 'business_number', 'type')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = (
            'url',
            'items',
            'client',
            'supplier',
            'received_date',
            'scheduled_deliver_date',
            'delivered_date',
            'status',
            'comments'
        )


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('url', 'order', 'item', 'quantity', 'price', 'comments')


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('url', 'orders', 'label', 'quantity', 'unit_price')


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'role', 'phone', 'email', 'address')
