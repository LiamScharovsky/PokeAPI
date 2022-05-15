from flask import Blueprint

bp = Blueprint('main', __name__, template_folder='main', url_prefix='/')
#bp works as BLueprint entry point
#name of file is main, the location of it is in the current file
#template folder to search of the HTML file and the url prefix

from .import routes 
#from current directory, import routes
#This tells blueprints to use routes


