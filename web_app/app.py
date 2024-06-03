#!/usr/bin/python3
""" Starts a Flash Web Application """
import requests
import json
from models import storage
from models.category import Category
from models.user import User
from models.product import Product
from os import environ, getenv

from flask import Flask, abort, render_template, request, redirect, session, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import uuid


app = Flask(__name__)
app.secret_key = getenv('AGRO_FLASK_SECRET')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

# Inject current_user into all templates
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@login_manager.user_loader
def load_user(user_id):
    return storage.find_user_by_email(user_id)


@app.route('/', strict_slashes=False)
def index():
    """ the index page of AgroMarket """
    url = getenv('AGRO_API_URL') + '/products'
    data = {}
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    return render_template('index.html', data=data, cache_id=str(uuid.uuid4()))

@app.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    """ The page for creating a user account """
    if request.method == 'POST':
        user_url = getenv('AGRO_API_URL') + '/users'
        image_url_template = getenv('AGRO_API_URL') + '/users/{}/image'

        data = request.form.to_dict()
        json_data = json.dumps(data)

        # Send POST request to create user
        user_response = requests.post(user_url, data=json_data, headers={'Content-Type': 'application/json'})

        if user_response.status_code == 201:
            user = user_response.json()
            user_id = user.get('id')

            # Retrieve the image
            file = request.files['file']
            files = {
                'file': (file.filename, file.read(), file.content_type)
            }

            # Send POST request to upload image
            image_url = image_url_template.format(user_id)
            image_response = requests.post(image_url, files=files)

            if image_response.status_code == 200:
                flash('Account created successfully', 'alert alert-success')
                return redirect(url_for('login_page'))
            else:
                flash('Image upload failed', 'alert alert-danger')
                # session['form_data'] = data  # Store form data in session
                return redirect(url_for('signup_page'))
        else:
            flash('Account creation failed, check the form', 'alert alert-danger')
            # session['form_data'] = data  # Store form data in session
            return redirect(url_for('signup_page'))
    else:
        # # Retrieve form data from session if available
        # form_data = session.pop('form_data', {})
        return render_template('signup.html', cache_id=str(uuid.uuid4()))


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login_page():
    """ the page for signing/logging in"""
    user = {}
    if request.method == 'POST':
        url = getenv('AGRO_API_URL') + '/login'
        data = request.form.to_dict()
        data_json = json.dumps(data)
        response = requests.post(url, data=data_json,
                                 headers={'Content-Type': 'application/json'})
        # print(f'Status code: {response.status_code}')
        if response.status_code == 200:
            user_data = response.json()
            user = User.from_dict(user_data)
            login_user(user)
            flash('Login successfully', 'alert alert-success')
            return redirect(url_for('index'))
        else:
            flash('Please check you login credentials', 'lert alert-danger')
            return redirect(url_for('login_page', data=user))
    return render_template('login.html', cache_id=str(uuid.uuid4()), data=user)

@login_required
@app.route('/profile', strict_slashes=False)
def profile():
    """ the page for user profile"""
    user = storage.find_user_by_email(current_user.email)

    return render_template('profile.html',
                           cache_id=str(uuid.uuid4()), user=user)

@login_required
@app.route('/product_index', strict_slashes=False)
def product_index():
    """ the page for product details"""
    user = storage.find_user_by_email(current_user.email)
    products = [product for product in user.products]

    return render_template('product_index.html', cache_id=str(uuid.uuid4()),
                           data=products)

@app.route('/products', strict_slashes=False,
           methods=['GET', 'POST'])
def products_page():
    """ the index page of product upload"""
    user = storage.find_user_by_email(current_user.email)
    if request.method == 'POST':
        if len(request.files.getlist('file')) > 5:
            flash('You can only upload 5 images', 'alert alert-danger')
            return redirect(url_for('products_page'))
        url = getenv('AGRO_API_URL') + '/products'
        data = request.form.to_dict()
        data['user_id'] = user.id
        
        data_json = json.dumps(data)
        response = requests.post(url, data=data_json,
                                 headers={'Content-Type': 'application/json'})
        if response.status_code == 201:
            new_product = response.json()
            url = getenv('AGRO_API_URL') + f'/products/{new_product["id"]}/images'
            files = [('file', (file.filename, file.read())) for file in
                     request.files.getlist('file')]
            response = requests.post(url, files=files)
            if response.status_code == 201:
                flash('Product uploaded Successfully', 'alert alert-success')
                return redirect(url_for('products_page'))
        else:
            flash('Product Upload failed', 'alert alert-danger')
            return redirect(url_for('products_page'))
    return render_template('product_upload.html', cache_id=str(uuid.uuid4()))

@login_required
@app.route('/product/<product_id>', strict_slashes=False, methods=['GET', 'POST', 'DELETE'])
def product_page(product_id):
    """ the page for product details of a particular product"""
    user = storage.find_user_by_email(current_user.email)
    url = getenv('AGRO_API_URL') + f'/products/{product_id}'

    if request.method == 'GET':
        response = requests.get(url)
        if response.status_code == 200:
            product = response.json()
            return render_template('product.html', cache_id=str(uuid.uuid4()), product=product, user=user)
        else:
            flash('Product not found', 'alert alert-danger')
            return redirect(url_for('product_index'))

    if request.method == 'POST':
        data = request.form.to_dict()
        data['user_id'] = user.id
        data_json = json.dumps(data)
        response = requests.put(url, data=data_json, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            flash('Product updated Successfully', 'alert alert-success')
        else:
            flash('Product update failed', 'alert alert-danger')
        return redirect(url_for('product_page', product_id=product_id))

    if request.method == 'DELETE':
        response = requests.delete(url)
        if response.status_code == 200:
            flash('Product deleted Successfully', 'alert alert-success')
            return redirect(url_for('product_index'))
        else:
            flash('Product deletion failed', 'alert alert-danger')
        return redirect(url_for('product_page', product_id=product_id))

    return render_template('product.html', cache_id=str(uuid.uuid4()), product=product, user=user)


@app.route('/products/<product_id>', strict_slashes=False)
def product_detail(product_id):
    """ the page for product details of a particular product"""
    url = getenv('AGRO_API_URL') + f'/products/{product_id}'
    image_url = getenv('AGRO_API_URL') + f'/products/{product_id}/images'

    response = requests.get(url)
    if response.status_code == 200:
        product = response.json()
        response = requests.get(image_url)
        if response.status_code == 200:
            product['images'] = response.json()
        return render_template('product_detail.html', cache_id=str(uuid.uuid4()), product=product)
    else:
        flash('Product not found', 'alert alert-danger')
        return redirect(url_for('index'))

@login_required
@app.route('/review', strict_slashes=False,
           methods=['GET', 'POST'])
def review_page():
    """ Returns the review of the user"""
    user = storage.find_user_by_email(current_user.email)
    reviews = user.reviews
    return render_template('review.html', data=reviews, cache_id=str(uuid.uuid4()))

@app.route('/account_type', strict_slashes=False)
def account_type():
    """ the page for account type selection"""

    return render_template('account_type.html', cache_id=str(uuid.uuid4()))

@app.route('/status_type', strict_slashes=False)
def status_type():
    """ the page for status type selection"""

    return render_template('status_type.html', cache_id=str(uuid.uuid4()))

@login_required
@app.route('/dashboard', methods=['GET', 'POST'], strict_slashes=False)
def sellers_dashboard():
    """ the page of the seller dashboard """
    user = storage.find_user_by_email(current_user.email)
    if request.method == 'POST':
        url = getenv('AGRO_API_URL') + '/sellers_dashboard'
        data = request.form.to_dict()
        data_json = json.dumps(data)
        response = requests.post(url, data=data_json,
                                headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            flash('Product uploaded Successfully', 'alert alert-success')
            new_product = response.json()
            return jsonify(new_product)
        else:
            flash('Upload failed, check the form', 'lert alert-danger')
            return jsonify({"error": "Upload failed"}), 400
    return render_template('seller_dashboard.html',
                           cache_id=str(uuid.uuid4()), data=user.products)

@login_required
@app.route('/orders', strict_slashes=False)
def orders():
    """ the page for orders"""
    user = storage.find_user_by_email(current_user.email)
    url = getenv('AGRO_API_URL') + f'/users/{user.id}/orders'
    response = requests.get(url)
    if response.status_code == 200:
        orders = response.json()
        return render_template('order.html', cache_id=str(uuid.uuid4()), data=orders)
    else:
        flash('Orders not found', 'alert alert-danger')
        return redirect(url_for('index'))

@login_required
@app.route('/cart/<product_id>', strict_slashes=False,
           methods=['GET', 'POST'])
def cart(product_id):
    """ retrieves the product and redirect to the cart route"""
    product = storage.get(Product, product_id)
    if not product:
        abort(404, description='Product not found')
    if request.method == 'POST':
        user = storage.find_user_by_email(current_user.email)
        data = request.form.to_dict()
        data['user_id'] = user.id
        data['product_id'] = product.id
        data_json = json.dumps(data)
        url = getenv('AGRO_API_URL') + '/orders'
        response = requests.post(url, data=data_json,
                                 headers={'Content-Type': 'application/json'})
        print(response.status_code)
        if response.status_code == 201:
            quantity = product.quantity - int(data['quantity'])
            product.quantity = quantity
            product.save()
            flash('Product added to cart successfully', 'alert alert-success')
            return redirect(url_for('product_detail', product_id=product_id))
        else:
            flash('Product not added to cart', 'alert alert-danger')
        return redirect(url_for('product_detail', product_id=product_id))
    return render_template('cart.html', cache_id=str(uuid.uuid4()),
                           product=product)

@app.route('/logout', strict_slashes=False)
def logout():
    """ the page for logging out"""
    logout_user()
    flash('Logout successfully', 'alert alert-success')
    return redirect(url_for('index'))


if __name__ == "__main__":
    """ start app """
    port = getenv('AGRO_API_PORT')
    host = getenv('AGRO_API_HOST')
    app.run(host, port=5000, debug=True)
