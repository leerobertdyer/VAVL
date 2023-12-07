from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .blueprints.venues import venues
app.register_blueprint(venues)

from . import routes, models