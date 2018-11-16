from api.models import Company, User, Order, Item, OrderItem, Contact, CompanyContact
from rest_framework import viewsets, response
from api.serializers import UserSerializer, CompanySerializer, ItemSerializer, OrderSerializer, OrderItemSerializers, ItemOrderSerializers, ContactSerializer


# Create your views here.

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(type='CLIENT').all()
    serializer_class = CompanySerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(type='SUPPLIER').all()
    serializer_class = CompanySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return OrderItem.objects.filter(order=self.kwargs['order_pk'])
    serializer_class = OrderItemSerializers


class ItemOrderViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return OrderItem.objects.filter(item=self.kwargs['item_pk'])
    serializer_class = ItemOrderSerializers
