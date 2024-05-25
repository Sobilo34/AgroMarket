#!/usr/bin/python3
"""  API actions for Product """
from werkzeug.utils import secure_filename
from models.user import User
from models.product import Product
from models.images import Image
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from flask import request
import os


@app_views.route('/products', methods=['GET'], strict_slashes=False)
@swag_from('documentation/products/all_products.yml')
def get_products():
    """
    Retrieves the list of all products objects
    """
    all_products = storage.all(Product).values()
    list_products = []
    for product in all_products:
        list_products.append(product.to_dict())
    return jsonify(list_products)


@app_views.route('/products/<product_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/products/get_product.yml', methods=['GET'])
def get_product(product_id):
    """ Retrieves an product """
    product = storage.get(Product, product_id)
    if not product:
        abort(404)

    return jsonify(product.to_dict())


@app_views.route('/products/<product_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/products/delete_product.yml', methods=['DELETE'])
def delete_product(product_id):
    """
    Deletes a product Object
    """

    product = storage.get(Product, product_id)

    if not product:
        abort(404)

    storage.delete(product)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/products', methods=['POST'], strict_slashes=False)
@swag_from('documentation/products/post_product.yml', methods=['POST'])
def post_product():
    """
    Creates a product
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    if 'description' not in request.get_json():
        abort(400, description="Missing description")
    if 'price' not in request.get_json():
        abort(400, description="Missing price")

    data = request.get_json()
    instance = Product(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/products/<product_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/products/put_product.yml', methods=['PUT'])
def put_product(product_id):
    """
    Updates a product
    """
    product = storage.get(Product, product_id)

    if not product:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(product, key, value)
    storage.save()
    return make_response(jsonify(product.to_dict()), 200)


@app_views.route('/products/<product_id>/images', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/products/images/get_images.yml', methods=['GET'])
def get_images(product_id):
    """ Retrieve images associated with a specific product. """
    product = storage.get(Product, product_id)
    if not product:
        abort(404)
    list_images = []
    for image in product.images:
        list_images.append(image.to_dict())

    return jsonify(list_images)


@app_views.route('/products/<product_id>/images', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/products/image/post_image.yml', methods=['POST'])
def post_image(product_id):
    """
    Upload images for a specific product.
    """
    UPLOAD_FOLDER = "web_app/static/images/upload"

    product = storage.get(Product, product_id)
    if not product:
        abort(404)
    if 'file' not in request.files:
        abort(400, description="Not a FILE")

    files = request.files.getlist('file')
    if not files:
        abort(400, description="No file uploaded")
    # get all the files
    image_urls = []
    for file in files:
        if file.filename == '':
            abort(400, description="No selected file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            print(filepath)
            file.save(filepath)

            # Create a new Image object
            new_image = Image(url=filename, product_id=product_id)
            new_image.save()
            image_urls.append(filepath)
        else:
            abort(400, description="Invalid file type")

    return jsonify(image_urls), 201


# helper function for post_images()
def allowed_file(filename):
    """
    Check if the file is allowed based on the file extension.
    """
    EXT = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXT
