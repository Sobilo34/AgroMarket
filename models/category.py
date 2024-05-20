#!/usr/bin/python
""" holds class Review"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Table, Integer, Text
from sqlalchemy.orm import relationship


# Association table for Users and Categories
user_category = Table(
                      'user_category', Base.metadata,
                      Column('user_id',  String(60), ForeignKey('users.id'),
                             primary_key=True),
                      Column('category_id', String(60),
                             ForeignKey('categories.id'), primary_key=True),
                             extend_existing=True
)


class Category(BaseModel, Base):
    """Representation of Category Model """
    __tablename__ = 'categories'
    name = Column(String(128), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    # Relationship to User model
    users = relationship('User', secondary=user_category,
                         back_populates='categories')

    def __init__(self, *args, **kwargs):
        """initializes Category"""
        super().__init__(*args, **kwargs)
