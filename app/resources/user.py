from app import app, db
from app.models import User, Contact
from flask_restful import Resource, marshal, reqparse, fields

user_fields = {
    "first_name": fields.String,
    "last_name": fields.String,
    "username": fields.String,
}


class UserResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=str, location='json')
        self.reqparse.add_argument('last_name', type=str, location='json')
        self.reqparse.add_argument('username', type=str, location='json')
        super(UserResource, self).__init__()

    def get(self, id):
        user = User.query.get_or_404(id)
        return {"user": marshal(user.jsonify(), user_fields)}

    def patch(self, id):
        user = User.query.get(id)
        return {"user": marshal(user.jsonify(), user_fields)}

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()

        return {"result": True, "id": id}


class UserListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=str, required=True, location='json')
        self.reqparse.add_argument('last_name', type=str, required=True, location='json')
        self.reqparse.add_argument('username', type=str, required=True, location='json')
        super(UserListResource, self).__init__()

    def get(self):
        users = User.query.all()
        return {"users": marshal([user.jsonify() for user in users], user_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        user = User()
        user.contact = Contact()

        user.contact.first_name = args["first_name"]
        user.contact.surname = args["last_name"]
        user.username = args["username"]

        db.session.add(user)
        db.session.commit()
        return {"user": marshal(user.jsonify(), user_fields)}
