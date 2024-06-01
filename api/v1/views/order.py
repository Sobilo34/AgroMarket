#!/usr/bin/python3
"""  API actions for Product """
from werkzeug.utils import secure_filename
from models.user import User
from models.product import Product
from models.order import Order
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from flask import request
import os


@app_views.route('/orders', methods=['GET'], strict_slashes=False)
@swag_from('documentation/orders/all_orders.yml')
def get_orders():
    """
    Retrieves the list of all orders objects
    """
    all_orders = storage.all(Order).values()
    list_orders = []
    for order in all_orders:
        list_orders.append(order.to_dict())
    return jsonify(list_orders)


@app_views.route('/orders/<order_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/orders/get_order.yml', methods=['GET'])
def get_order(order_id):
    """ Retrieves an order """
    order = storage.get(Order, order_id)
    if not order:
        abort(404)

    return jsonify(order.to_dict())


@app_views.route('/orders/<order_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/orders/delete_order.yml', methods=['DELETE'])
def delete_order(order_id):
    """
    Deletes a order Object
    """

    order = storage.get(Order, order_id)

    if not order:
        abort(404)

    storage.delete(order)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/orders', methods=['POST'], strict_slashes=False)
@swag_from('documentation/orders/post_order.yml', methods=['POST'])
def post_order():
    """
    Creates an order
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'product_id' not in request.get_json():
        abort(400, description="Missing product_id")
    if 'quantity' not in request.get_json():
        abort(400, description="Missing quantity")
    if 'total_price' not in request.get_json():
        abort(400, description="Missing total_price")

    data = request.get_json()
    instance = Order(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/orders/<order_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/orders/put_order.yml', methods=['PUT'])
def put_order(order_id):
    """
    Updates a order
    """
    order = storage.get(Order, order_id)

    if not order:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(order, key, value)
    storage.save()
    return make_response(jsonify(order.to_dict()), 200)

@app_views.route('/orders/<order_id>/reviews', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/orders/get_reviews.yml', methods=['GET'])
def get_reviews(order_id):
    """ Retrieves an order reviews """
    order = storage.get(Order, order_id)
    if not order:
        abort(404)

    return jsonify(order.reviews.to_dict())

@app_views.route('/orders/<order_id>/reviews', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/orders/get_reviews.yml', methods=['POST'])
def post_reviews(order_id):
    """ Creates review for an order """
    order = storage.get(Order, order_id)
    if not order:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'rating' not in request.get_json():
        abort(400, description="Missing rating")
    if 'comment' not in request.get_json():
        abort(400, description="Missing comment")

    data = request.get_json()
    data['order_id'] = order.id
    instance = Review(**data)
    instance.save() 

    return jsonify(instance.to_dict())
