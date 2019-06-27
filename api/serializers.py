from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework import serializers
from api.models import ApiUser, Company, CompanyContact, Order, Item, Contact, OrderItem, State
from django.utils import timezone


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ApiUser
        fields = ('url', 'username', 'contact', 'email', 'company')


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
        contact_list_data = validated_data.pop('contacts')
        company = Company.objects.create(**validated_data)
        for contact_data in contact_list_data:
            contact = Contact.objects.create(**contact_data)
            CompanyContact.objects.create(company=company, contact=contact)
        return company


class OrderItemSerializers(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'order_pk': 'order__pk',
    }

    item = serializers.HyperlinkedRelatedField(
        view_name='item-detail',
        many=False,
        read_only=False,
        queryset=Item.objects.all()
    )

    class Meta:
        model = OrderItem
        fields = ('item', 'quantity', 'unit_price', 'comments')


class ItemOrderSerializers(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'item_pk': 'item__pk',
    }

    order = serializers.HyperlinkedRelatedField(
        view_name='order-detail',
        many=False,
        read_only=True,
    )

    class Meta:
        model = OrderItem
        fields = ('order', 'quantity', 'unit_price', 'comments')


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    client = serializers.HyperlinkedRelatedField(
        view_name="company-detail",
        many=False,
        read_only=False,
        queryset=Company.objects.all()
    )

    supplier = serializers.HyperlinkedRelatedField(
        view_name="company-detail",
        many=False,
        read_only=False,
        queryset=Company.objects.filter(type='SUPPLIER')
    )

    status = serializers.SlugRelatedField(
        slug_field='title',
        many=False,
        read_only=False,
        queryset=State.objects.all()
    )

    items = OrderItemSerializers(many=True, read_only=False)

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

    def create(self, validated_data):
        item_list_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        order.received_date = timezone.now()
        for item_data in item_list_data:
            order_item = OrderItem.objects.create(order=order, **item_data)
            order_item.unit_price = order_item.item.unit_price
            order_item.save()
        order.save()
        return order


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('url', 'orders', 'label', 'quantity', 'unit_price')

    orders = ItemOrderSerializers(many=True, read_only=True)


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'role', 'phone', 'email', 'address')


class StateSerializer(serializers.HyperlinkedModelSerializer):
    previous_state = serializers.SlugRelatedField(
        slug_field='title',
        many=False,
        read_only=False,
        required=False,
        queryset=State.objects.all(),
        allow_null=True
    )

    class Meta:
        model = State
        fields = ('url', 'label', 'title', 'description', 'previous_state', 'next_state')
