from .database import db
from datetime import datetime


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
            'price': self.price,
            'image': self.image
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    pizza = db.relationship('Pizza')

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'pizza_id': self.pizza_id,
            'pizza_name': self.pizza.name if self.pizza else None,
            'quantity': self.quantity,
        }
    
    @property
    def calculated_item_total(self):
        return self.quantity * self.pizza.price



class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'phone_number': self.phone_number,
            'total_price': self.total_price,
            'created_at': self.created_at,
            'items': [item.to_dict() for item in self.items]
        }
