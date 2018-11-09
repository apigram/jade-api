"""Jade URL Configuration"""
from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'item', views.ItemViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'client', views.ClientViewSet)
router.register(r'supplier', views.SupplierViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
