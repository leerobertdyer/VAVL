from flask import render_template
from app import app
import requests
from bs4 import BeautifulSoup


@app.route('/eagle')
def eagle():
    url = "https://www.thegreyeagle.com/calendar/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    if resp.status_code == 200:
        showDivs = soup.find_all("div", class_="rhpSingleEvent")
        for show in showDivs:
            print(show, end="\n\n")
    else:
        print(f"Failed to retrieve page. Status code: {resp.status_code}")
    return render_template('home.html')