#!/usr/bin/python3
"""  API actions for Deliveries. """
from api.v1.views import app_views
from models.delivery import Delivery
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/deliveries', methods=['Get'], strict_slashes=False)
def get_deliveries():
    """Retrieve the list of all deliveries in the database."""
    all_deliveries = storage.all(Delivery).values()
    list_deliveries = []
    for delivery in all_deliveries:
        list_deliveries.append(delivery.to_dict())
    return jsonify(list_deliveries)


@app_views.route('/deliveries', method=['POST'], strict_slashes=False)
def post_deliveries():
    """
    Create new delivery
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    if  'delivery_date' not in request.json():
        abort(400, description="Missing Delivery Date")
    if 'delivered' not in request.get_json():
        abort(400, description="Missing Delivered")
    if 'address' not in request.get_json():
        abort(400, description="Missing Address")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing User id")
    if 'order_id' not in request.get_json():
        abort(400, description="Missing Order id")

    data = request.get_json()
    instance = Delivery(**data)
    instance.set_delivery_date(data.get('delivery_date'))
    instance.set_delivered(data.get('delivered'))
    # instance.set_order(data.get('order_id'))
    instance.set_address(data.get('address'))
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/deliveries/<id>', method=['Get'], strict_slashers=False)
def view_user_delivery(id):
    """
    Retrieve specific delivery by ID.
    """
    delivery = storage.get(delivery, id)

    if not delivery:
        abort(404)

    return jsonify(delivery.to_dict())


@app_views.route('/deliveries/<id>', methods=['PUT'], strict_slashes=False)
def update_delivery(id):
    """
    Updates a specific delivery by ID
    """
    user = storage.get(Delivery, id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'order_id', 'user_id', 'created_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route("/deliveries/<id>", methods=["DELECT"], strict_slashes=False)
def delete_delivery(id):
    """
    Delete a specific id in deliveries.
    """
    delivery = storage.get(Delivery, id)

    if not delivery:
        abort(404)
    
    storage.delete(delivery)
    storage.save()

    return make_response(jsonify({}), 200)
