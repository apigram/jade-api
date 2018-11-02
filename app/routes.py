from app import app
from flask_restful import Api

from app.resources.user import UserResource, UserListResource
from app.resources.item import ItemResource, ItemListResource
from app.resources.order import OrderResource, OrderListResource
from app.resources.client import ClientResource, ClientListResource
from app.resources.supplier import SupplierResource, SupplierListResource

api = Api(app)

# Item Resources
api.add_resource(ItemListResource, '/jade/api/item', endpoint='items')
api.add_resource(ItemResource, '/jade/api/item/<int:id>', endpoint='item')

# Order Resources
api.add_resource(OrderListResource, '/jade/api/order', endpoint='orders')
api.add_resource(OrderResource, '/jade/api/order/<int:id>', endpoint='order')

# Client Resources
api.add_resource(ClientListResource, '/jade/api/client', endpoint='clients')
api.add_resource(ClientResource, '/jade/api/client/<int:id>', endpoint='client')

# Supplier Resources
api.add_resource(SupplierListResource, '/jade/api/supplier', endpoint='suppliers')
api.add_resource(SupplierResource, '/jade/api/supplier/<int:id>', endpoint='supplier')

# User resources
api.add_resource(UserListResource, '/jade/api/user', endpoint='users')
api.add_resource(UserResource, '/jade/api/user/<int:id>', endpoint='user')
