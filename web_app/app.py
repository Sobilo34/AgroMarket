#!/usr/bin/python3
""" Starts a Flash Web Application """
import requests
import json
from models import storage
from models.category import Category
from models.user import User
from os import environ, getenv
from flask import Flask, render_template, request, redirect, url_for, flash
import uuid


app = Flask(__name__)
app.secret_key = getenv('AGRO_FLASK_SECRET')


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False)
def index():
    """ the index page of AgroMarket """

    return render_template('index.html', cache_id=str(uuid.uuid4()))

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
            flash('Account created successfully', 'success')
            return redirect(url_for('login_page'))
        else:
            flash('Account creation failed, check the form', 'danger')
            return redirect(url_for('signup_page', data=data))
    return render_template('signup.html', cache_id=str(uuid.uuid4()))

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login_page():
    """ the page for signing/logging in"""
    if request.method == 'POST':
        url = getenv('AGRO_API_URL') + '/login'
        data = request.form.to_dict()
        data_json = json.dumps(data)
        response = requests.post(url, data=data_json,
                                 headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            print('login successfully')
            flash('Account created successfully', 'success')
            return redirect(url_for('login_page'))
        else:
            flash('Account creation failed, check the form', 'danger')
            return redirect(url_for('signup_page', data=data))
    return render_template('login.html', cache_id=str(uuid.uuid4()))

@app.route('/account_type', strict_slashes=False)
def account_type():
    """ the page for account type selection"""

    return render_template('account_type.html', cache_id=str(uuid.uuid4()))

@app.route('/status_type', strict_slashes=False)
def status_type():
    """ the page for status type selection"""

    return render_template('status_type.html', cache_id=str(uuid.uuid4()))

@app.route('/dashboard', strict_slashes=False)
def sellers_dashboard():
    """ the page of the seller dashboard """

    return render_template('seller_dashboard.html', cache_id=str(uuid.uuid4()))

@app.route('/products', strict_slashes=False)
def products_page():
    """ the index page of prduct upload"""

    return render_template('product.html', cache_id=str(uuid.uuid4()))


if __name__ == "__main__":
    """ start app """
    port = getenv('AGRO_API_PORT')
    host = getenv('AGRO_API_HOST')
    app.run(host, port)
