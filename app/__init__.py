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

if render:
    indexURL = 'https://vavl.onrender.com'
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path = '/opt/render/project/.render/chrome/opt/google/chrome', headless=True)
        driver = browser.new_page() 
else:
    indexURL = 'http://127.0.0.1:5000'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        driver = browser.new_page() 

from .blueprints.venues import venues
app.register_blueprint(venues)

from . import routes, models