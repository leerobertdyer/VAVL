from flask import Flask, render_template
from config import Config
import requests

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    URL = "https://realpython.github.io/fake-jobs/"
    page = requests.get(URL)
    print(page.text)
    return render_template('home.html')