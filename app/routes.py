from flask import render_template
from .models import Event
from app import app

def helper(allEvents):
    lastDate = allEvents[0].show_date.strftime('%B %-d, %Y')
    events = []
    for e in allEvents:
        if e.show_date != lastDate:
            events.append({'newDate': e.show_date.strftime('%B %-d, %Y')})
            lastDate = e.show_date
        events.append({'venue': e.venue, 'title': e.title, 'tickets': e.tickets, 'image': e.image})
    return events
            

@app.route('/')
def home():
    e = Event.query.order_by(Event.show_date).all()
    lastDate = e[0].show_date
    events = helper(e)
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
    
