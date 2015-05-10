from flask import Blueprint

conference = Blueprint('conference', __name__)

from . import views
