from flask import render_template
from app import app, db
import requests
from bs4 import BeautifulSoup
from .models import Event
from datetime import datetime

@app.route('/')
def home():
    events = Event.query.order_by(Event.show_date).all()
    return render_template('home.html', events=events)

@app.route('/sort-by-eagle')
def eagleSort():
    events = Event.query.filter_by(venue='Grey Eagle').all()
    return render_template('home.html', events=events)

@app.route('/sort-by-peel')
def peelSort():
    events = Event.query.filter_by(venue='Orange Peel').all()
    return render_template('home.html', events=events)

@app.route('/sort-by-rabbit')
def rabbitSort():
    events = Event.query.filter_by(venue='Rabbit Rabbit').all()
    return render_template('home.html', events=events)

@app.route('/sort-by-salvage')
def salvageSort():
    events = Event.query.filter_by(venue='Salvage Station').all()
    return render_template('home.html', events=events)

@app.route('/sort-by-cherokee')
def cherokeeSort():
    events = Event.query.filter_by(venue='Harrah\'s Cherokee').all()
    return render_template('home.html', events=events)
    

@app.route('/eagle')
def eagle():
    
    url = "https://www.thegreyeagle.com/calendar/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    eagleEvents = []
    showYear = ''
    if resp.status_code == 200:
        mainDiv = soup.find("div", class_="rhp-desktop-list")
        for child in mainDiv.children:
            if child.name == "span":
               showYear = child.span.text[-4::].strip()
            elif child.name == "div":
                try:
                    showDay = child.find(id="eventDate").text.strip()
                    showDateStr = showDay + " " + showYear
                    try:
                        showDate = datetime.strptime(showDateStr, "%a, %b %d %Y")
                    except:
                        showDate = datetime.strptime(showDateStr, "%a, %B %d %Y")
                except:
                    showDate = "Date Not Found"
                try:
                    showTitle = child.find(id="eventTitle").find('h2').text
                except:
                    showTitle = "Title not found"
                try:
                    showImage = child.find("img", class_="eventListImage")['src'] 
                except:
                    showImage = "app/static/sad.jpg"
                try:
                    showTickets = child.find(id="eventTitle")["href"]
                except:
                    showTickets = "Tickets Not Found"
                eagleEvents.append({
                    "showDate": showDate, 
                    "showTitle": showTitle, 
                    "showImage": showImage, 
                    "showTickets": showTickets})
        for show in eagleEvents:
            existing_event = Event.query.filter_by(title=show["showTitle"], show_date=show["showDate"]).first()
            if existing_event is None:
                new_event = Event(
                    venue = "Grey Eagle",
                    title = show["showTitle"],
                    show_date = show["showDate"],
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
    showYear = ''
    if resp.status_code == 200:
        mainDiv = soup.find("div", class_="rhp-desktop-list")
        for child in mainDiv:
            if child.name == "span":
                showYear = child.span.text[-4::].strip()
            elif child.name == "div":
                try:
                    showDay = child.find(id="eventDate").text.strip() 
                    showDateStr = showDay + " " + showYear
                    if showDateStr[5:9].upper() == "SEPT":
                        showDateStr = showDateStr[0:8] + showDateStr[9::]
                    showDate = datetime.strptime(showDateStr, "%a, %b %d %Y")
                except:
                    showDate = "Date Not Found"
                try:
                    showTitle = child.find(id="eventTitle").find('h2').text.strip()
                except:
                    showTitle = "Title not found"
                try:
                    showImage = child.find("img", class_="eventListImage")['src'] 
                except:
                    showImage = "app/static/sad.jpg"
                try:
                    showTickets = child.find(id="eventTitle")["href"]
                except:
                    showTickets = "Tickets Not Found"
                peelEvents.append({
                    "showDate": showDate, 
                    "showTitle": showTitle, 
                    "showImage": showImage, 
                    "showTickets": showTickets})
        for show in peelEvents:
            existing_event = Event.query.filter_by(title=show["showTitle"], show_date=show["showDate"]).first()
            if existing_event is None:
                new_event = Event(
                    venue = "Orange Peel",
                    title = show["showTitle"],
                    show_date = show["showDate"],
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
                showDateStr = dateAndTime[:-9].strip()
                print(showDateStr)
                showDate = datetime.strptime(showDateStr, "%B %d, %Y")
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
                showTickets = show.find("h3", class_="tribe-events-calendar-list__event-title").find("a")['href']
            except:
                showTickets = "Tickets Not Found"
            rabbitEvents.append({
                "showDate": showDate, 
                "showTitle": showTitle, 
                "showImage": showImage, 
                "showTickets": showTickets})
        for show in rabbitEvents:
            existing_event = Event.query.filter_by(title=show["showTitle"], show_date=show["showDate"]).first()
            if existing_event is None:
                new_event = Event(
                    venue = "Rabbit Rabbit",
                    title = show["showTitle"],
                    show_date = show["showDate"],
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
                if len(showDay) < 5:
                    print('Too Short!')
                    alternateDate = show.find("div", class_="event-subtitle").text.strip()
                    print('alt date: ', alternateDate)
                    for char in alternateDate:
                        if char.isdigit():
                            showDay += " " + char
                            break
                showDate = showDay + " 2024"
                print('final showDate: ', showDate)
                            
            except:
                showDate = "Date Not Found"
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
            existing_event = Event.query.filter_by(title=show["showTitle"], show_date=show["showDate"]).first()
            if existing_event is None:
                new_event = Event(
                    venue = "Harrah's Cherokee",
                    title = show["showTitle"],
                    show_date = show["showDate"],
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
                showDateStr = f"{showDay} {showMonth} {showNum} {showYear}"
                showDate = datetime.strptime(showDateStr, "%a %b %d %Y")
            except:
                showDate = "Date/time Not Found"
            try:
                showTitle = show.find("div", class_="event-list-title").text.strip()
            except:
                showTitle = "Title not found"
            try:
                showImage = show.find("a", class_="event-list-image")["style"][23:-3]
            except:
                showImage = "app/static/sad.jpg"
            try:
                showTickets = show.find("div", class_="event-list-titles").find("a")["href"]
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
                show_date = show["showDate"],
                tickets = show["showTickets"],
                image = show["showImage"]
            )
            db.session.add(new_event)
            db.session.commit()
    else:
        print(f"Failed to retrieve page. Status code: {resp.status_code}")
    return salvageEvents
    
    