from flask import Blueprint

index_bp = Blueprint('index', __name__)
recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

from . import index, recipe
