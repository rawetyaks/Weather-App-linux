# -*- coding: utf-8 -*-

# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Configure Jinja2 to load templates for the application
from jinja2 import Environment, PackageLoader

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

from codecs import encode, decode

app.jinja_env.filters['encode'] = encode
app.jinja_env.filters['decode'] = decode

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable
from app.tu_weather.controllers import tu_weather as tu_module

# Register blueprint(s)
app.register_blueprint(tu_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.drop_all()
db.create_all()

# Initialize all the data in the database.
from tu_weather.scripts import load_translations_to_db as load
load(db)