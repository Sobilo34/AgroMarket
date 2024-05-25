#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Boolean, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from hashlib import md5
from models.order import Order
from models.product import Product
from models.category import user_category, Category
import bcrypt


class User(BaseModel, Base):
    """Representation of a user data """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        phone = Column(String(15), nullable=False)
        profile_pic = Column(Text, nullable=True)
        is_farmer = Column(Boolean, default=False)
        is_admin = Column(Boolean, default=False)
        farm_name = Column(String(100), nullable=True)
        location = Column(String(100), nullable=True)
        products = relationship('Product', back_populates='user')
        orders = relationship('Order', back_populates='user')
        reviews = relationship('Review', back_populates='user')
        images = relationship('Image', back_populates='user')
        deliveries = relationship('Delivery', back_populates='user')

        # Relationship to Category model
        categories = relationship('Category', secondary=user_category,
                                  back_populates='users')

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

    def set_password(self, password):
        """ hashes the user password using bycript """
        self._password = bcrypt.hashpw(password.encode('utf-8'),
                                       bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """ checkes the hashed password for authentication """
        return bcrypt.checkpw(password.encode('utf-8'),
                              self._password.encode('utf-8'))

    def make_admin(self):
        """Makes the user an admin"""
        self.is_admin = True

    def remove_admin(self):
        """Removes admin privileges from the user"""
        self.is_admin = False

    def make_farmer(self):
        """Makes the user a farmer"""
        self.is_farmer = True

    def remove_farmer(self):
        """Removes farmer status from the user"""
        self.is_farmer = False
