#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.category import Category
from models.user import User
from os import environ, getenv
from flask import Flask, render_template
import uuid


app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False)
def index():
    """ the index page of AgroMarket """

    return render_template('index.html', cache_id=str(uuid.uuid4()))

@app.route('/signup', strict_slashes=False)
def signup_page():
    """ the page for signing/logging in"""

    return render_template('login.html', cache_id=str(uuid.uuid4()))

@app.route('/login', strict_slashes=False)
def login_page():
    """ the page for signing/logging in"""

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
