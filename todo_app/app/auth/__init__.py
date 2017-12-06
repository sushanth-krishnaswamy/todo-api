# auth/__init__.py

from flask import Blueprint

# Instance iof the authentication blueprint

auth_blueprint = Blueprint('auth', __name__)

from . import views
