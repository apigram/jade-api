from api.models import Company, User, Order, Item, OrderItem
from rest_framework import viewsets
from api.serializers import UserSerializer, CompanySerializer, ItemSerializer, OrderSerializer, OrderItemSerializer


# Create your views here.

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
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
