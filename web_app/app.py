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

    return render_template('index.html', cache_id = str(uuid.uuid4()))

@app.route('/dashboard', strict_slashes=False)
def sellers_dashboard():
    """ the index page of the seller """

    return render_template('seller_dashboard.html', cache_id = str(uuid.uuid4()))


if __name__ == "__main__":
    """ start app """
    port = getenv('AGRO_API_PORT')
    host = getenv('AGRO_API_HOST')
    app.run(host, port)
