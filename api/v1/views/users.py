#!/usr/bin/python3
"""  API actions for Users """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from flask import request
import os
from werkzeug.utils import secure_filename


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    """
    Retrieves the list of all user objects
    or a specific user
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/login', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/login_user.yml', methods=['POST'])
def login_user():
    """
    Logs in a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json() and 'phone' not in request.get_json():
        abort(400, description="Missing email or phone")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    user = None
    if email:
        user = storage.find_user_by_email(email)
    elif phone:
        user = storage.find_user_by_email(phone)

    if not user or not user.check_password(password):
        abort(401, description="Invalid email/phone or password")

    return make_response(user.to_dict(), 200)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    """ Retrieves an user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user Object
    """

    user = storage.get(User, user_id)
    if not user:
        abort(404, description="User not found")

    image_path = os.path.join('web_app/static/images/upload/profile',
                              user.profile_pic if user.profile_pic else '')
    
    # Check if the image exists
    if os.path.exists(image_path):
        try:
            os.remove(image_path)
        except Exception as e:
            abort(404, description=f"Error deleting image: {e}")
    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])

def post_user():
    """
    Creates a user without file upload
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    required_fields = ['email', 'first_name', 'last_name', 'password', 'phone']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # check if user already exists
    if storage.find_user_by_email(data.get('email')):
        abort(409, description="User already exists")
    instance = User(**data)
    instance.set_password(data.get('password'))
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def put_user(user_id):
    """
    Updates a user
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at', 'password']

    data = request.get_json()
    for key, value in data.items():
        if key == 'password' and value != '':
            user.set_password(value)
        elif key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route('/users/<user_id>/orders', methods=['GET'])
@swag_from('documentation/user/orders.yml', methods=['GET'])
def get_user_orders(user_id):
    """ retrieves all orders of a user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    orders = user.orders
    list_orders = []

    for order in orders:
        obj = order.to_dict()

        # Add user information to the order dictionary
        user = {
            'id': order.user.id,
            'email': order.user.email,
            'phone': order.user.phone,
            'first_name': order.user.first_name,
            'last_name': order.user.last_name,
            'address': order.user.location
        }
        obj['user'] = user

        # Add product information to the order dictionary
        product = {
            'id': order.product.id,
            'name': order.product.name,
            'description': order.product.description,
            'price': order.product.price,
            'image': order.product.cover_img
        }
        obj['product'] = product

        list_orders.append(obj)

    return jsonify(list_orders)

@app_views.route('/users/<user_id>/image', methods=['POST'])
@swag_from('documentation/user/upload_image.yml', methods=['POST'])
def upload_image(user_id):
    """
    Uploads an image for a specific user
    """
    UPLOAD_FOLDER = "web_app/static/images/upload/profile"
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if 'file' not in request.files:
        abort(401, description="Not a FILE")

    file = request.files['file']
    if file.filename == '':
        abort(404, description="No selected file")
    if not allowed_file(file.filename):
        abort(404, description="Invalid file type")

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    user.profile_pic = filepath.split('/')[-1]
    storage.save()

    return make_response(jsonify(user.to_dict()), 200)

# helper function for post_images()
def allowed_file(filename):
    """
    Check if the file is allowed based on the file extension.
    """
    EXT = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXT
