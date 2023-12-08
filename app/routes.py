from flask import render_template
from .models import Event
from app import app
from datetime import datetime

def helper(allEvents):
    lastDate = allEvents[0].show_date.date()
    today = datetime.now().date()
    i = 0
    while lastDate < today:
        i += 1
        lastDate = allEvents[i].show_date.date()
    events = []
    events.append({'newDate': lastDate.strftime('%B %-d, %Y')})
    x = 0
    while x <= i:
        events.append({'venue': allEvents[x].venue, 'title': allEvents[x].title, 'tickets': allEvents[x].tickets, 'image': allEvents[x].image})
        x += 1
    for e in allEvents:
        if e.show_date.date() > lastDate:
            events.append({'newDate': e.show_date.strftime('%B %-d, %Y')})
            lastDate = e.show_date.date()
            events.append({'venue': e.venue, 'title': e.title, 'tickets': e.tickets, 'image': e.image})
    return events
            

@app.route('/')
def home():
    e = Event.query.order_by(Event.show_date).all()
    events = helper(e)
    lastDate = events[0]
    return render_template('home.html', events=events, lastDate=lastDate)


@app.route('/sort-by-eagle')
def eagleSort():
    e = Event.query.filter_by(venue='Grey Eagle').all()
    lastDate = e[0].show_date
    events = helper(e)
    return render_template('home.html', events=events, lastDate=lastDate)

@app.route('/sort-by-peel')
def peelSort():
    e = Event.query.filter_by(venue='Orange Peel').all()
    lastDate = e[0].show_date
    events = helper(e)
    return render_template('home.html', events=events, lastDate=lastDate)

@app.route('/sort-by-rabbit')
def rabbitSort():
    e = Event.query.filter_by(venue='Rabbit Rabbit').all()
    lastDate = e[0].show_date
    events = helper(e)
    return render_template('home.html', events=events, lastDate=lastDate)

@app.route('/sort-by-salvage')
def salvageSort():
    e = Event.query.filter_by(venue='Salvage Station').all()
    lastDate = e[0].show_date
    events = helper(e)
    return render_template('home.html', events=events, lastDate=lastDate)

@app.route('/sort-by-cherokee')
def cherokeeSort():
    e = Event.query.filter_by(venue='Harrah\'s Cherokee').all()
    lastDate = e[0].show_date
    events = helper(e)
    return render_template('home.html', events=events, lastDate=lastDate)
    
