from app import app, db
from app.models import Company
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
        return {"supplier": marshal(supplier, supplier_fields)}