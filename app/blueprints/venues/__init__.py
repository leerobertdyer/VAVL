from flask import Blueprint

venues = Blueprint('venues', __name__)

from . import routes