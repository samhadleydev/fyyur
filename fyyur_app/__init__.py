#____________________________________________________________________________________
#                                                                             IMPORTS
from flask import Flask, render_template
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import dateutil.parser
import babel
import logging
import os
from logging import Formatter, FileHandler
#____________________________________________________________________________________
#                                                                              CONFIG
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('fyyur_app.config')
db = SQLAlchemy(app)

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# DONE: IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://samhadleydev:1234@localhost:5432/fyyur_app'
#____________________________________________________________________________________
#                                                                             FILTERS
def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime
#____________________________________________________________________________________
#                                                                              ROUTES
from fyyur_app import models, venue_routes, artist_routes, show_routes

@app.route('/')
def index():
    return render_template('pages/home.html')
#____________________________________________________________________________________
#                                                                              ERRORS
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')
