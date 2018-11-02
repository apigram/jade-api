from app import app, db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer)
    username = db.Column(db.String(100))

    contact = db.relationship('Contact')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def jsonify(self):
        return {
            "id": self.id,
            "first_name": self.contact.first_name,
            "last_name": self.contact.last_name,
            "username": self.username,
        }


# Represents an order made by a client. This will also track delivery information.
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer)
    supplier_id = db.Column(db.Integer)
    received_date = db.Column(db.DateTime)
    scheduled_deliver_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)
    status = db.Column(db.String(100))
    comments = db.Column(db.Text)

    client = db.relationship('Client', back_populates='orders')
    supplier = db.relationship('Supplier', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order')

    def __repr__(self):
        return '<Order {}>'.format(self.id)

    def jsonify(self):
        return {
            "id": self.id,
        }


# Represents a single item for an order.
# Because a single order from one supplier can contain multiple different items, each item will have their own quantity.
class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    price = db.Column(db.String)
    comments = db.Column(db.Text)

    order = db.relationship('Order', back_populates='items')
    item = db.relationship('Item', back_populates='orders')

    def __repr__(self):
        return '<OrderItem {}>'.format(self.id)

    def jsonify(self):
        return {
            "id": self.id,
        }


# A single supply item.
class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

    orders = db.relationship('OrderItem', back_populates='item')

    def __repr__(self):
        return '<Item {}>'.format(self.id)

    def jsonify(self):
        return {
            "id": self.id,
        }


# Both suppliers and clients are businesses
class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    business_number = db.Column(db.String(100))  # In Australia this would be the ABN.

    contacts = db.relationship('Contact', back_populates='company')
    orders = db.relationship('Order', back_populates='client')
    clients = db.relationship('SupplierClient', back_populates='supplier')
    suppliers = db.relationship('SupplierClient', back_populates='client')

    def __repr__(self):
        return '<Client {}>'.format(self.id)

    def jsonify(self):
        return {
            "id": self.id,
        }


class CompanyContact(db.Model):
    __tablename__ = 'company'
    contact_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)

    contact = db.relationship('Contact')
    company = db.relationship('Company', back_populates='contacts')

    def __repr__(self):
        return '<CompanyClient {}>'.format(self.id)

    def jsonify(self):
        return {
            "contact_id": self.id,
        }


class SupplierClient(db.Model):
    __tablename__ = 'supplier_client'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer)
    client_id = db.Column(db.Integer)

    supplier = db.relationship('Company', back_populates='clients')
    client = db.relationship('Company', back_populates='suppliers')

    def __repr__(self):
        return '<Client {}>'.format(self.id)

    def jsonify(self):
        return {
            "id": self.id,
        }


class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))

    def __repr__(self):
        return '<Contact {}>'.format(self.id)

    def jsonify(self):
        return {
            "id": self.id,
        }
