from app import app, db
from app.models import Item
from flask_restful import Resource, marshal, fields, reqparse

item_fields = {
    "label": fields.String
}

class ItemResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('label', type=str, location='json')
        self.reqparse.add_argument('quantity', type=str, location='json')
        super(ItemResource, self).__init__()

    def get(self, id):
        item = Item.query.get_or_404(id)
        return {"item": marshal(item, item_fields)}

    def put(self, id):
        item = Item.query.get_or_404(id)
        return {"item": marshal(item, item_fields)}

    def delete(self, id):
        item = Item.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {"result": True, "id": id}


class ItemListResource(Resource):
    def get(self):
        items = Item.query.all()
        return {"items": marshal([item for item in items], item_fields)}

    def post(self):
        item = Item()
        return {"item": marshal(item, item_fields)}