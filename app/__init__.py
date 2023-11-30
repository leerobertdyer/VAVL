from flask import Flask, render_template
from config import Config
import requests

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    URL = "https://www.thegreyeagle.com/calendar/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get(URL, headers=headers)
    if resp.status_code == 200:
        # print(resp.text)
        pass
    else:
        print(f"Failed to retrieve page. Status code: {resp.status_code}")
    return render_template('home.html')