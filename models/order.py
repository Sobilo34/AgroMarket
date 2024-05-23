#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Boolean, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Order(BaseModel, Base):
    """Representation of an order data and methods"""
    __tablename__ = 'orders'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    product_id = Column(String(60), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    
    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')
    delivery = relationship('Delivery', uselist=False, back_populates='order')
    reviews = relationship('Review', back_populates='order')

    def __init__(self, *args, **kwargs):
        """Initializes order"""
        super().__init__(*args, **kwargs)

    def set_user(self, user):
        """Sets the user for the order"""
        self.user_id = user.id

    def set_product(self, product):
        """Sets the product for the order"""
        self.product_id = product.id

    def set_quantity(self, quantity):
        """Sets the quantity for the order"""
        self.quantity = quantity

    def set_total_price(self, total_price):
        """Sets the total price for the order"""
        self.total_price = total_price