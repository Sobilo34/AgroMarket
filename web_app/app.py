#!/usr/bin/python3
""" Starts a Flash Web Application """
import requests
import json
from models import storage
from models.category import Category
from models.user import User
from models.product import Product
from os import environ, getenv

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
def signup_page():
    """ the page for creating a user account """
    if request.method == 'POST':
        url = getenv('AGRO_API_URL') + '/users'
        data = request.form.to_dict()
        data_json = json.dumps(data)
        response = requests.post(url, data=data_json,
                                 headers={'Content-Type': 'application/json'})
        if response.status_code == 201:
            print('account created')
            flash('Account created successfully', 'success')
            return redirect(url_for('login_page'))
        else:
            flash('Account creation failed, check the form', 'danger')
            return redirect(url_for('signup_page', data=data))
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
            print(f'User is active: {current_user.is_active}')
            print(f'user email: {current_user.email}')
            flash('Login successfully', 'alert alert-success')
            return redirect(url_for('index'))
        else:
            flash('Please check you login credentials', 'lert alert-danger')
            return redirect(url_for('login_page', data=user))
    return render_template('login.html', cache_id=str(uuid.uuid4()), data=user)


@app.route('/products', strict_slashes=False)
def products_page():
    """ the index page of product upload"""
    return render_template('product.html', cache_id=str(uuid.uuid4()))


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
    return render_template('seller_dashboard.html', cache_id=str(uuid.uuid4()))

@app.route('/profile', strict_slashes=False)
def profile():
    """ the page for user profile"""

    return render_template('profile.html', cache_id=str(uuid.uuid4()))

@app.route('/cart>', strict_slashes=False)
def cart():
    """ the page for product details"""

    return render_template('cart.html', cache_id=str(uuid.uuid4()))

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
    app.run(host, port=5000)
