from flask import Blueprint

root = Blueprint('root', __name__)
from flaskr.routes import *