from app import app
from flask_restful import Api

from app.resources.user import UserResource, UserListResource
from app.resources.item import ItemResource, ItemListResource, OrderListByItemResource
from app.resources.order import OrderResource, OrderListResource, ItemListByOrderResource, OrderItemResource
from app.resources.client import ClientResource, ClientListResource
from app.resources.supplier import SupplierResource, SupplierListResource, SupplierClientResource

api = Api(app)

# Item Resources
api.add_resource(ItemListResource, '/jade/api/item', endpoint='items')
api.add_resource(ItemResource, '/jade/api/item/<int:id>', endpoint='item')
api.add_resource(OrderListByItemResource, '/jade/api/item/<int:id>/order', endpoint='order_list_by_item')

# Order Resources
api.add_resource(OrderListResource, '/jade/api/order', endpoint='orders')
api.add_resource(OrderResource, '/jade/api/order/<int:id>', endpoint='order')
api.add_resource(ItemListByOrderResource, '/jade/api/order/<int:id>/item', endpoint='item_list_by_order')
api.add_resource(OrderItemResource, '/jade/api/order/<int:order_id>/item/<int:item_id>', endpoint="order_item")

# Client Resources
api.add_resource(ClientListResource, '/jade/api/client', endpoint='clients')
api.add_resource(ClientResource, '/jade/api/client/<int:id>', endpoint='client')
api.add_resource(SupplierClientResource, '/jade/api/client/<int:client_id>/supplier/<int:supplier_id>', endpoint="supplier_client")

# Supplier Resources
api.add_resource(SupplierListResource, '/jade/api/supplier', endpoint='suppliers')
api.add_resource(SupplierResource, '/jade/api/supplier/<int:id>', endpoint='supplier')
api.add_resource(SupplierClientResource, '/jade/api/supplier/<int:supplier_id>/client/<int:client_id>', endpoint="client_supplier")

# User resources
api.add_resource(UserListResource, '/jade/api/user', endpoint='users')
api.add_resource(UserResource, '/jade/api/user/<int:id>', endpoint='user')
