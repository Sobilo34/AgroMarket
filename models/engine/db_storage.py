#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from models.user import User
from models.category import Category
from models.product import Product
from models.order import Order
from models.delivery import Delivery
from models.review import Review
from models.images import Image
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"User": User, "Category": Category, "Product": Product,
           "Order": Order, "Delivery": Delivery, "Review": Review, "Image": Image}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        AGRO_MYSQL_USER = getenv('AGRO_MYSQL_USER')
        AGRO_MYSQL_PWD = getenv('AGRO_MYSQL_PWD')
        AGRO_MYSQL_HOST = getenv('AGRO_MYSQL_HOST')
        AGRO_MYSQL_DB = getenv('AGRO_MYSQL_DB')
        AGRO_ENV = getenv('AGRO_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(AGRO_MYSQL_USER,
                                             AGRO_MYSQL_PWD,
                                             AGRO_MYSQL_HOST,
                                             AGRO_MYSQL_DB))
        if AGRO_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        for clss in classes:
            if cls is classes[clss] or cls is clss:
                all_cls = self.all(cls)
                for value in all_cls.values():
                    if (value.id == id):
                        return value

        return None
    
    def find_user_by_email(self, email):
        """
        Find user by email, or None if not found
        """
        if not email:
            return None

        all_users = self.all(User)
        for user in all_users.values():
            if (user.email == email):
                return user

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(self.all(clas).values())
        else:
            count = len(self.all(cls).values())

        return count
