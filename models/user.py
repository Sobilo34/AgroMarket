#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Boolean, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from hashlib import md5
from models.category import user_category, Category


class User(BaseModel, Base):
    """Representation of a user data """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        phone = Column(String(15), nullable=True)
        profile_pic = Column(Text, nullable=True)
        is_farmer = Column(Boolean, default=False)
        farm_name = Column(String(100), nullable=True)
        location = Column(String(100), nullable=True)
        category_id = Column(String(60), ForeignKey('categories.id'),
                             nullable=True)

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
