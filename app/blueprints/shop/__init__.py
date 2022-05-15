from flask import Blueprint

bp = Blueprint('shop', __name__, template_folder='shop', url_prefix='shop')
#name the blueprint, tell it where the file is, find template folder for HTML
#and get its URL

from .import routes
#from same folder, get routes