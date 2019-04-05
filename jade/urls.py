"""Jade URL Configuration"""
from django.conf.urls import url, include
from rest_framework_nested import routers
from api import views


router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'item', views.ItemViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'client', views.ClientViewSet, basename='client')
router.register(r'supplier', views.SupplierViewSet, basename='supplier')
router.register(r'contact', views.ContactViewSet)
router.register(r'state', views.StateViewSet)

order_router = routers.NestedDefaultRouter(router, r'order', lookup='order')
order_router.register(r'item', views.OrderItemViewSet, base_name='order-item')

item_router = routers.NestedDefaultRouter(router, r'item', lookup='item')
item_router.register(r'order', views.ItemOrderViewSet, base_name='item-order')

client_router = routers.NestedDefaultRouter(router, r'client', lookup='company')
client_router.register(r'contact', views.CompanyContactViewSet, base_name='client_contact')

supplier_router = routers.NestedDefaultRouter(router, r'supplier', lookup='company')
supplier_router.register(r'contact', views.CompanyContactViewSet, base_name='supplier_contact')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(order_router.urls)),
    url(r'^', include(item_router.urls)),
    url(r'^', include(client_router.urls)),
    url(r'^', include(supplier_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.CustomAuthToken.as_view())
]
