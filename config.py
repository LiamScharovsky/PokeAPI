import os
from re import S
from dotenv import load_dotenv                          #allows to go search variables
basedir = os.path.abspath(os.path.dirname(__name__))    #os.path.abspath feeds the current directory of the file we're in
                                                        #os.path.dirname returns directory name we're interested in getting
                                                        #__name__gets the name of the file we're in now
                                                        #path from the directory we need stuff from to the one we're in
load_dotenv(os.path.join(basedir,'.env'))               #joins base directory of first argument with the file name of where our directories are


class Config:
    FLASK_APP = os.getenv('FLASK_APP')               #allows to get data from .env by calling the variable
    FLASK_ENV = os.getenv('FLASK_ENV')               #make sure you pass the variable as a name
    if os.getenv('SQLALCHEMY_DATABASE_URI').startswith('postgres'): #change postgres to postgresql in the .env
        SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI').replace('postgres', 'postgresql')  # Another reference to .env
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_SERVER =os.getenv('MAIL_SERVER')
    MAILPORT = os.getenv('MAILPORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAILUSERNAME = os.getenv('MAILUSERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_RECIPIENT = os.getenv('MAIL_RECIPIENT')

