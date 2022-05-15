from flask import Blueprint

bp = Blueprint('blog', __name__, template_folder= 'users', url_prefix='blog')



from .import routes, models