from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework import serializers
from api.models import User, Company, CompanyContact, Order, Item, Contact, OrderItem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'contact', 'email')


class CompanyContactsSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'contact_pk': 'contact__pk'
    }

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'role', 'phone', 'email', 'address')


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('url', 'name', 'contacts', 'business_number', 'type')

    contacts = CompanyContactsSerializer(many=True, read_only=False)

    def create(self, validated_data):
        client_data = validated_data
        del client_data['contacts']
        contact_list_data = validated_data['contacts']
        company = Company(**client_data)
        company.save()
        for contact_data in contact_list_data:
            contact = CompanyContact(**contact_data)
            contact.company = company
            contact.save()
        return company


class OrderItemSerializers(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'order_pk': 'order__pk'
    }

    class Meta:
        model = OrderItem
        fields = ('url', 'order', 'item', 'quantity', 'price', 'comments')


class ItemOrderSerializers(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'item_pk': 'item__pk'
    }

    class Meta:
        model = OrderItem
        fields = ('url', 'order', 'item', 'quantity', 'price', 'comments')


class OrderCompanySerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'order_pk': 'order__pk'
    }

    class Meta:
        model = Company
        fields = ('url', 'name', 'contacts', 'business_number', 'type')

    contacts = CompanyContactsSerializer(many=True, read_only=True)


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    client = serializers.HyperlinkedRelatedField(
        view_name="client-detail",
        lookup_field='client_pk',
    )
    supplier = serializers.HyperlinkedRelatedField(
        view_name="supplier-detail",
        lookup_field='supplier_pk',
    )

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
    items = OrderItemSerializers(many=True, read_only=False)


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('url', 'orders', 'label', 'quantity', 'unit_price')

    orders = OrderItemSerializers(many=True, read_only=True)


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'role', 'phone', 'email', 'address')
