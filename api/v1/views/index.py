#!/usr/bin/python3
""" Index api that returns the status and stats for all our tables """
from models.category import Category
from models.user import User
from models.product import Product
from models.order import Order
from models.review import Review
from models.delivery import Delivery
from models.images import Image
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = [User, Category, Product, Order, Delivery, Review, Image]
    names = ["User", "Category", "Product", "Order", "Delivery", "Review",
             "Image"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)
