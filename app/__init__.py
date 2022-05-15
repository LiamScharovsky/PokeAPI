#Entry point to module/package. It isntantiate flask application
from flask import Flask
from config import Config
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail



moment = Moment()
db = SQLAlchemy()           #Object Relational Mapper
migrate = Migrate()         #Handle transaction of database
login = LoginManager()  # handle login session
mail = Mail()   #handles sending mail


def createApp(configClass=Config):      
    app = Flask(__name__)
    app.config.from_object(configClass)          #tell the app to use the configurations we set 
    moment.init_app(app)                        #Tells flask to use moments
    db.init_app(app)                            #database takes the app
    migrate.init_app(app, db)                   #migration takes both the transformation and the app
    login.init_app(app)                         #opens session when user logs in and saves data                       
    mail.init_app(app)
    with app.app_context():                     #while working under the app context, the below happens
        from app.blueprints.main import bp as main_bp  #import blueprint functionality from main __init__
        app.register_blueprint(main_bp)         #register the main bp blueprints
    
        from app.blueprints.shop import bp as shop_bp #import shop's blueprint
        app.register_blueprint(shop_bp)             #render the shop_bp blueprint 
        
        from app.blueprints.blog import bp as blog_bp
        app.register_blueprint(blog_bp)

        from app.blueprints.main import errors
        
    return app                                  #return the instance
