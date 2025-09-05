from datetime import datetime
from . import db

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    cep = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='pending', nullable=False)
    total = db.Column(db.Float, default=0.0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')

    def to_dict(self, include_items=True):
        data = {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'cep': self.cep,
            'address': self.address,
            'status': self.status,
            'total': round(self.total, 2),
            'created_at': self.created_at.isoformat() + 'Z',
        }
        if include_items:
            data['items'] = [item.to_dict() for item in self.items]
        return data

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'title': self.title,
            'price': round(self.price, 2),
            'quantity': self.quantity,
            'subtotal': round(self.price * self.quantity, 2),
        }
