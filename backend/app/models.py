"""
Database models for the Pizza Delivery API
"""
from .database import db
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates
import re

class Pizza(db.Model):
    """Pizza model representing available pizzas"""
    __tablename__ = 'pizza'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    ingredients = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('price > 0', name='check_positive_price'),
        CheckConstraint('length(name) > 0', name='check_non_empty_name'),
        CheckConstraint('length(ingredients) > 0', name='check_non_empty_ingredients'),
    )
    
    # Relationships
    order_items = db.relationship('OrderItem', back_populates='pizza', lazy='dynamic')
    
    @validates('name')
    def validate_name(self, key, name):
        """Validate pizza name"""
        if not name or not name.strip():
            raise ValueError('Pizza name cannot be empty')
        if len(name.strip()) > 100:
            raise ValueError('Pizza name cannot exceed 100 characters')
        return name.strip()
    
    @validates('price')
    def validate_price(self, key, price):
        """Validate pizza price"""
        if price <= 0:
            raise ValueError('Pizza price must be positive')
        if price > 1000:
            raise ValueError('Pizza price cannot exceed $1000')
        return price
    
    @validates('ingredients')
    def validate_ingredients(self, key, ingredients):
        """Validate pizza ingredients"""
        if not ingredients or not ingredients.strip():
            raise ValueError('Pizza ingredients cannot be empty')
        if len(ingredients.strip()) > 500:
            raise ValueError('Pizza ingredients cannot exceed 500 characters')
        return ingredients.strip()
    
    def to_dict(self):
        """Convert pizza to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
            'price': float(self.price),
            'image': self.image
        }

class OrderItem(db.Model):
    """Order item model representing individual items in an order"""
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, index=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id', ondelete='RESTRICT'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_positive_quantity'),
        CheckConstraint('quantity <= 50', name='check_max_quantity'),
    )
    
    # Relationships
    order = db.relationship('Orders', back_populates='items')
    pizza = db.relationship('Pizza', back_populates='order_items')
    
    @validates('quantity')
    def validate_quantity(self, key, quantity):
        """Validate order item quantity"""
        if quantity <= 0:
            raise ValueError('Quantity must be positive')
        if quantity > 50:
            raise ValueError('Quantity cannot exceed 50')
        return quantity
    
    def to_dict(self):
        """Convert order item to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'pizza_id': self.pizza_id,
            'pizza_name': self.pizza.name if self.pizza else None,
            'quantity': self.quantity,
            'calculated_item_total': float(self.calculated_item_total)
        }
    
    @property
    def calculated_item_total(self) -> Decimal:
        """Calculate item total price"""
        if self.pizza:
            return round(self.quantity * self.pizza.price, 2)
        return Decimal('0.00')

class Orders(db.Model):
    """Order model representing customer orders"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False, index=True)
    phone_number = db.Column(db.String(20), nullable=False, index=True)
    total_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Constraints
    __table_args__ = (
        CheckConstraint('total_price >= 0', name='check_non_negative_total'),
        CheckConstraint('length(customer_name) > 0', name='check_non_empty_customer_name'),
        CheckConstraint('length(phone_number) > 0', name='check_non_empty_phone'),
    )
    
    # Relationships
    items = db.relationship('OrderItem', back_populates='order', lazy='dynamic', cascade='all, delete-orphan')
    
    @validates('customer_name')
    def validate_customer_name(self, key, name):
        """Validate customer name"""
        if not name or not name.strip():
            raise ValueError('Customer name cannot be empty')
        if len(name.strip()) > 100:
            raise ValueError('Customer name cannot exceed 100 characters')
        return name.strip()
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone):
        """Validate phone number format"""
        if not phone or not phone.strip():
            raise ValueError('Phone number cannot be empty')
        
        # Basic phone number validation (international format)
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not phone_pattern.match(phone.strip()):
            raise ValueError('Phone number must be in valid international format')
        
        return phone.strip()
    
    @validates('total_price')
    def validate_total_price(self, key, price):
        """Validate total price"""
        if price < 0:
            raise ValueError('Total price cannot be negative')
        if price > 10000:
            raise ValueError('Total price cannot exceed $10,000')
        return price
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'phone_number': self.phone_number,
            'total_price': float(self.total_price),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'items': [item.to_dict() for item in self.items]
        }
    
    def update_total_price(self):
        """Update the order's total price based on its items"""
        total = sum(item.calculated_item_total for item in self.items)
        self.total_price = round(total, 2)
        self.updated_at = datetime.now(timezone.utc)
    
    @property
    def item_count(self) -> int:
        """Get total number of items in the order"""
        return self.items.count()
    
    @property
    def is_empty(self) -> bool:
        """Check if order has no items"""
        return self.item_count == 0
