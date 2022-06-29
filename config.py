import os
from dotenv import load_dotenv

load_dotenv()


# scr customizations
class AppConfigs:
    SECRET_KEY = os.getenv('secretkey', '')
    adminRegister = os.getenv('nameuseradmin', '') + os.getenv('firstnameadmin', '') + os.getenv('lastnameadmin',
                                                                                                 '') + os.getenv(
        'emailadmin', '')


# scr configure
class Config(AppConfigs):
    # compare faces path
    compareFacesPath = "/home/elalocador/Desktop/facial_comparate/Register/application/scr/CompareFaces"
    unknownPersons = "/home/elalocador/Desktop/facial_comparate/Register/application/scr/CompareFaces/UnknownPersons"

    # config route the templates folder  and others statics pages
    TEMPLATE_FOLDER = '/home/elalocador/Desktop/facial_comparate/Register/application/scr/views/templates/'
    STATIC_FOLDER = '/home/elalocador/Desktop/facial_comparate/Register/application/scr/views/static/'
    host = 'localhost'
    user = os.getenv('user', '')
    password = os.getenv('password', '')
    database = os.getenv('database', '')

    # config to flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI = 'mysql://' + user + ':' + password + '@' + host + '/' + database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


'''
scr's configure
'''
