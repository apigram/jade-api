from app import db
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
    "price": fields.String,
    "comments": fields.String
}


class OrderResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('client_id', type=int, location='json')
        self.reqparse.add_argument('supplier_id', type=int, location='json')
        self.reqparse.add_argument('received_date', type=datetime, location='json')
        self.reqparse.add_argument('scheduled_delivery_date', type=datetime, location='json')
        self.reqparse.add_argument('delivered_date', type=datetime, location='json')
        self.reqparse.add_argument('order_comments', type=str, location='json')
        self.reqparse.add_argument('status', type=str, location='json')
        self.reqparse.add_argument('item_id', type=int, location='json')
        self.reqparse.add_argument('quantity', type=int, location='json')
        self.reqparse.add_argument('price', type=float, location='json')
        self.reqparse.add_argument('order_item_comments', type=str, location='json')
        super(OrderResource, self).__init__()

    def get(self, id):
        order = Order.query.get_or_404(id)
        return {"order": marshal(order, order_fields)}

    def post(self, id):
        args = self.reqparse.parse_args()
        order_item = OrderItem()
        order_item.order_id = id

        db.session.add(order_item)
        db.session.commit()

        return {"order_item": marshal(order_item, order_item_fields)}

    def put(self, id):
        args = self.reqparse.parse_args()
        order = Order.query.get_or_404(id)
        for key, val in args.items():
            order[key] = val
        db.session.commit()
        return {"order": marshal(order, order_fields)}

    def patch(self, id):
        args = self.reqparse.parse_args()
        order = Order.query.get_or_404(id)
        for key, val in args.items():
            order[key] = val
        return {"order": marshal(order, order_fields)}

    def delete(self, id):
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return {"result": True, "id": id}


class OrderListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('client_id', type=int, location='json')
        self.reqparse.add_argument('supplier_id', type=int, location='json')
        self.reqparse.add_argument('scheduled_delivery_date', type=datetime, location='json')
        self.reqparse.add_argument('comments', type=str, location='json')
        super(OrderListResource, self).__init__()

    def get(self):
        order = Order.query.all()
        return {"orders": marshal(order, order_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        order = Order()
        db.session.add(order)
        db.session.commit()
        return {"order": marshal(order, order_fields)}


class ItemListByOrderResource(Resource):
    def get(self, order_id):
        order_items = Order.query.get_or_404(order_id)
        return {"order_items": marshal([order_item for order_item in order_items], order_item_fields)}


class OrderItemResource(Resource):
    def delete(self, order_id, item_id):
        order_item = OrderItem.query.filter_by(order_id=order_id, item_id=item_id).first_or_404()
        order_item_id = order_item.id
        db.session.delete(order_item)
        db.session.commit()

        return {"result": True, "id": order_item_id}
