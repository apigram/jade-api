from app import db
from app.models import Company
from flask_restful import Resource, marshal, fields, reqparse

client_fields = {
    "name": fields.String,
    "business_number": fields.String,
    "suppliers": fields.Url('supplier_list_by_client')
}


class ClientResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('business_number', type=str, location='json')
        super(ClientResource, self).__init__()

    def get(self, id):
        client = Company.query.get_or_404(id)
        return {"client": marshal(client, client_fields)}

    def put(self, id):
        client = Company.query.get_or_404(id)
        return {"client": marshal(client, client_fields)}

    def delete(self, id):
        client = Company.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        return {"result": True, "id": id}


class ClientListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('business_number', type=str, location='json')
        super(ClientListResource, self).__init__()

    def get(self):
        clients = Company.query.all()
        return {"clients": marshal([client for client in clients], client_fields)}

    def post(self):
        client = Company()
        db.session.add(client)
        db.session.commit()
        return {"client": marshal(client, client_fields)}
