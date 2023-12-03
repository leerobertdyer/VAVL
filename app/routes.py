from flask import render_template
from app import app, db
import requests
from bs4 import BeautifulSoup
from .models import Event
import datetime

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/eagle')
def eagle():
    
    url = "https://www.thegreyeagle.com/calendar/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    eagleEvents = []
    
    if resp.status_code == 200:
        showDivs = soup.find_all("div", class_="rhpSingleEvent")
        for show in showDivs:
            try:
                showDay = show.find(id="eventDate").text 
                showYear = show.find("span", class_="rhp-events-list-separator-month").text[-4:]
                showDate = showDay + " " + showYear
            except:
                showDate = "Date Not Found"
            try:
                showTitle = show.find(id="eventTitle").find('h2').text
            except:
                showTitle = "Title not found"
            try:
                showImage = show.find("img", class_="eventListImage")['src'] 
            except:
                showImage = "app/static/sad.jpg"
            try:
                showTickets = show.find(id="ctaspan-44637").find("a")['href']
            except:
                showTickets = "Tickets Not Found"
            eagleEvents.append({
                "showDate": showDate, 
                "showTitle": showTitle, 
                "showImage": showImage, 
                "showTickets": showTickets})
        for show in eagleEvents:
            new_event = Event(
                venue = "Grey Eagle",
                title = show["showTitle"],
                show_date = datetime.strptime(show["showDate"], "%a, %b %d %Y"),
                tickets = show["showTickets"],
                image = show["showImage"],
            )
            db.session.add(new_event)
            db.session.commit()
    else:
        print(f"Failed to retrieve page. Status code: {resp.status_code}")
    return eagleEvents

@app.route('/peel')
def peel():
    
    url = "https://theorangepeel.net/events/?view=list"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    peelEvents = []
    
    if resp.status_code == 200:
        showDivs = soup.find_all("div", class_="rhpSingleEvent")
        for show in showDivs:
            try:
                showDay = show.find(id="eventDate").text 
                showYear = show.find('span', class_="rhp-events-list-separator-month").text[-4:]
                showDate = showDay + " " + showYear
            except:
                showDate = "Date Not Found"
            try:
                showTitle = show.find(id="eventTitle").find('h2').text
            except:
                showTitle = "Title not found"
            try:
                showImage = show.find("img", class_="eventListImage")['src'] 
            except:
                showImage = "app/static/sad.jpg"
            try:
                showTickets = show.find("div", class_="rhp-event-list-cta").find("a")['href']
            except:
                showTickets = "Tickets Not Found"
            peelEvents.append({
                "showDate": showDate, 
                "showTitle": showTitle, 
                "showImage": showImage, 
                "showTickets": showTickets})
        for show in peelEvents:
            new_event = Event(
                venue = "Orange Peel",
                title = show["showTitle"],
                show_date = datetime.strptime(show["showDate"], "%a, %b %d %Y"),
                tickets = show["showTickets"],
                image = show["showImage"],
            )
            db.session.add(new_event)
            db.session.commit()
    else:
        print(f"Failed to retrieve page. Status code: {resp.status_code}")
    return peelEvents



@app.route('/rabbit')
def rabbit():
    
    url = "https://rabbitrabbitavl.com/calendar/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    rabbitEvents = []
    
    if resp.status_code == 200:
        showDivs = soup.find_all("div", class_="tribe-events-calendar-list__event-row")
        for show in showDivs:
            try:
                dateAndTime = show.find("span", class_="tribe-event-date-start").text 
                showDate = dateAndTime[:-9]
            except:
                showDate = "Date/time Not Found"
            try:
                showTitle = show.find("h3", class_="tribe-events-calendar-list__event-title").find("a")['title']
            except:
                showTitle = "Title not found"
            try:
                showImage = show.find("img", class_="tribe-events-calendar-list__event-featured-image")['src'] 
            except:
                showImage = "app/static/sad.jpg"
            try:
                showTickets = show.find("div", class_="prc-tribe-list-links").find("a")['href']
            except:
                showTickets = "Tickets Not Found"
            rabbitEvents.append({
                "showDate": showDate, 
                "showTitle": showTitle, 
                "showImage": showImage, 
                "showTickets": showTickets})
        for show in rabbitEvents:
            new_event = Event(
                venue = "Rabbit Rabbit",
                title = show["showTitle"],
                show_date = datetime.strptime(show["showDate"], "%B %d, %Y"),
                tickets = show["showTickets"],
                image = show["showImage"]
            )
            db.session.add(new_event)
            db.session.commit()
    else:
        print(f"Failed to retrieve page. Status code: {resp.status_code}")
    return rabbitEvents

@app.route('/cherokee')
def cherokee():
    url = 'https://www.harrahscherokeecenterasheville.com/events-tickets/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    cherokeeEvents = []
    
    if resp.status_code == 200:
        showDivs = soup.find_all("div", class_="list-view")
        
        for show in showDivs:
            try:
                showDay = show.find("div", class_="event-date").text.strip()
                showDate = showDay + " 2024"
            except:
                showDate = "Jan 1, 1955"
            try:
                showTitle = show.find("div", class_="event-details").find("h3").text
            except:
                showTitle = "Title not found"
            try:
                showImage = show.find("div", class_="image-wrapper").find("img")['src'] 
            except:
                showImage = "app/static/sad.jpg"
            try:
                showTickets = show.find("a", class_="event-ticket")['href']
            except:
                showTickets = "Tickets Not Found"
            cherokeeEvents.append({
                "showDate": showDate, 
                "showTitle": showTitle, 
                "showImage": showImage, 
                "showTickets": showTickets})
        for show in cherokeeEvents:
            new_event = Event(
                venue = "Harrah's Cherokee",
                title = show["showTitle"],
                show_date = datetime.strptime(show["showDate"], "%b %d, %Y"),
                tickets = show["showTickets"],
                image = show["showImage"]
            )
            db.session.add(new_event)
            db.session.commit()
    else:
        print(f"Failed to retrieve page. Status code: {resp.status_code}")
    return cherokeeEvents
    
    
@app.route('/salvage')
def salvage():
    url = 'https://salvagestation.com/events/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    salvageEvents = []
    
    if resp.status_code == 200:
        showDivs = soup.find_all("div", class_="event-list-wrapper")
        
        for show in showDivs:
            try:
                showDay = show.find("div", class_="event-list-day").text.strip()
                showMonth = show.find("div", class_="event-list-month").text.strip()
                showNum = show.find("div", class_="event-list-number").text.strip()
                showYear = show.find("div", class_="event-list-year").text.strip()
                showDate = f"{showDay} {showMonth} {showNum} {showYear}"
            except:
                showDate = "Date/time Not Found"
            try:
                showTitle = show.find("div", class_="event-list-title").text
            except:
                showTitle = "Title not found"
            try:
                showImage = show.find("a", class_="event-list-image")["style"][23:-3]
            except:
                showImage = "app/static/sad.jpg"
            try:
                showTickets = show.find("a", class_="event-list-button buy")['href']
            except:
                showTickets = "Tickets Not Found"
            salvageEvents.append({
                "showDate": showDate, 
                "showTitle": showTitle, 
                "showImage": showImage, 
                "showTickets": showTickets})
        for show in salvageEvents:
            new_event = Event(
                venue = "Salvage Station",
                title = show["showTitle"],
                show_date = datetime.strptime(show["showDate"], "%a, %b, %d, %Y"),
                tickets = show["showTickets"],
                image = show["showImage"]
            )
            db.session.add(new_event)
            db.session.commit()
    else:
        print(f"Failed to retrieve page. Status code: {resp.status_code}")
    return salvageEvents
    
    