from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework import serializers
from api.models import User, Company, CompanyContact, Order, Item, Contact, OrderItem
import copy


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'contact', 'email')


class CompanyContactsSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'company_pk': 'company__pk'
    }

    contact = serializers.HyperlinkedRelatedField(
        view_name='contact-detail',
        many=False,
        read_only=True
    )

    class Meta:
        model = CompanyContact
        fields = ('contact',)


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('url', 'name', 'business_number', 'type', 'contacts')

    contacts = CompanyContactsSerializer(many=True, read_only=False)

    def create(self, validated_data):
        client_data = copy.deepcopy(validated_data)
        del client_data['contacts']
        contact_list_data = validated_data['contacts']
        company = Company(**client_data)
        company.save()
        for contact_data in contact_list_data:
            contact = Contact(**contact_data)
            contact.save()
            companycontact = CompanyContact()
            companycontact.company = company
            companycontact.contact = contact
            companycontact.save()
        return company


class ClientSerializer(CompanySerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='client-detail',
        lookup_field='pk'
    )


class SupplierSerializer(CompanySerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='supplier-detail',
        lookup_field='pk'
    )


class OrderItemSerializers(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'order_pk': 'order__pk'
    }

    order = serializers.HyperlinkedRelatedField(
        view_name='order-detail',
        many=False,
        read_only=True
    )

    item = serializers.HyperlinkedRelatedField(
        view_name='item-detail',
        many=False,
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ('order', 'item', 'quantity', 'unit_price', 'comments')


class ItemOrderSerializers(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'item_pk': 'item__pk'
    }

    order = serializers.HyperlinkedRelatedField(
        view_name='order-detail',
        many=False,
        read_only=True
    )

    item = serializers.HyperlinkedRelatedField(
        view_name='item-detail',
        many=False,
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ('order', 'item', 'quantity', 'price', 'comments')


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
        many=False,
        read_only=False,
        queryset=Company.objects.filter(type='CLIENT')
    )
    supplier = serializers.HyperlinkedRelatedField(
        view_name="supplier-detail",
        many=False,
        read_only=False,
        queryset=Company.objects.filter(type='SUPPLIER')
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

    def create(self, validated_data):
        order_data = copy.deepcopy(validated_data)
        del order_data['items']
        item_list_data = validated_data['items']
        order = Order(**order_data)
        order.save()
        for item_data in item_list_data:
            order_item = OrderItem(**item_data)
            order_item.order = order
            order_item.save()
        return order


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('url', 'orders', 'label', 'quantity', 'unit_price')

    orders = OrderItemSerializers(many=True, read_only=True)


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'role', 'phone', 'email', 'address')
