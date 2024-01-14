from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
import os
from playwright.sync_api import sync_playwright

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

render = os.environ.get('RENDER') == 'true'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel="chrome") 
    driver = browser.new_page()  

if render:
    indexURL = 'https://vavl.onrender.com'
else:
    indexURL = 'http://127.0.0.1:5000'

from .blueprints.venues import venues
app.register_blueprint(venues)

from . import routes, models