from flask import Flask
from flask_migrate import Migrate
from config import Config
from .routes import global_scope
from flask_sqlalchemy import SQLAlchemy
from .models import db

# initialization app
app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)
app.config.from_object(Config)

# instances
SQLAlchemy(app)
migrate = Migrate(app, db)

# create tables
with app.app_context():
    db.create_all()

# blueprints
app.register_blueprint(global_scope, url_prefix='/')
