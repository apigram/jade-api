from app import db
from app.models import Company, SupplierClient
from flask_restful import Resource, marshal, fields

supplier_fields = {
    "name": fields.String,
    "business_number": fields.String,
    "clients": fields.Url('client_list_by_supplier')
}


class SupplierResource(Resource):
    def get(self, id):
        supplier = Company.query.get_or_404(id)
        return {"supplier": marshal(supplier, supplier_fields)}

    def put(self, id):
        supplier = Company.query.get_or_404(id)
        return {"supplier": marshal(supplier, supplier_fields)}

    def delete(self, id):
        supplier = Company.query.get_or_404(id)
        db.session.delete(supplier)
        db.session.commit()
        return {"result": True, "id": id}


class SupplierListResource(Resource):
    def get(self):
        suppliers = Company.query.all()
        return {"suppliers": marshal([supplier for supplier in suppliers], supplier_fields)}

    def post(self):
        supplier = Company()
        db.session.add(supplier)
        db.session.commit()
        return {"supplier": marshal(supplier, supplier_fields)}


class SupplierClientResource(Resource):
    def delete(self, supplier_id, client_id):
        supplier_client = SupplierClient.query.filter_by(supplier_id=supplier_id, client_id=client_id).first_or_404()
        supplier_client_id = supplier_client.id
        db.session.delete(supplier_client)
        db.session.commit()

        return {"result": True, "id": supplier_client_id}