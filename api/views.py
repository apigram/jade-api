from api.models import Company, User, Order, Item, OrderItem, Contact, CompanyContact
from rest_framework import viewsets, response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from api.serializers import UserSerializer, ClientSerializer, SupplierSerializer, ItemSerializer, OrderSerializer, OrderItemSerializers, CompanyContactsSerializer, ItemOrderSerializers, ContactSerializer


# Create your views here.

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(type='CLIENT').all()
    serializer_class = ClientSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(type='SUPPLIER').all()
    serializer_class = SupplierSerializer


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
        return OrderItem.objects.filter(order=self.kwargs['order_pk']).all()
    serializer_class = OrderItemSerializers


class ItemOrderViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return OrderItem.objects.filter(item=self.kwargs['item_pk']).all()
    serializer_class = ItemOrderSerializers


class CompanyContactViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return CompanyContact.objects.filter(company=self.kwargs['company_pk'])
    serializer_class = CompanyContactsSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            }
        })
