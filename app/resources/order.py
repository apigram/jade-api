from app import app, db
from app.models import Order, OrderItem
from flask_restful import Resource, marshal, fields, reqparse
import datetime

order_fields = {
    "uri": fields.Url("order"),
    "client": fields.Url("client"),
    "supplier": fields.Url("supplier"),
    "items": fields.Url("item_list_by_order"),
    "received_date": fields.DateTime,
    "scheduled_delivery_date": fields.DateTime,
    "delivered_date": fields.DateTime,
    "status": fields.String,
    "comments": fields.String
}

order_item_fields = {
    "uri": fields.Url("order_item"),
    "order": fields.Url('order'),
    "item": fields.Url('item'),
    "quantity": fields.Integer,
    "comments": fields.String
}


class OrderResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('client_id', type=int, location='json')
        self.reqparse.add_argument('supplier_id', type=int, location='json')
        self.reqparse.add_argument('scheduled_delivery_date', type=datetime, location='json')
        self.reqparse.add_argument('comments', type=str, location='json')
        super(OrderResource, self).__init__()

    def get(self, id):
        order = Order.query.get_or_404(id)
        return {"order": marshal(order, order_fields)}

    def post(self, id):
        order_item = OrderItem()
        order_item.order_id = id

        return {"item": marshal(order_item, order_item_fields)}

    def put(self, id):
        order = Order.query.get_or_404(id)
        return {"order": marshal(order, order_fields)}

    def delete(self, id):
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return {"result": True, "id": id}


class OrderListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('business_number', type=str, location='json')
        super(OrderListResource, self).__init__()

    def get(self):
        order = Order.query.all()
        return {"orders": marshal(order, order_fields)}

    def post(self):
        order = Order()
        return {"order": marshal(order, order_fields)}
