from flask import render_template, request, jsonify
from .models import Event
from app import app
from datetime import datetime, date
from app import db

def helper(allEvents):
    if not allEvents:
        return []  # Return an empty list if allEvents is empty
    today = datetime.now().date()
    events = []
    process_events = False
    lastDate = None
    for event in allEvents:
        event_date = event.show_date.date()
        if event_date >= today:
            process_events = True

        if process_events:
            if lastDate is None or event_date > lastDate:
                lastDate = event_date
                events.append({'newDate': lastDate.strftime('%B %-d, %Y')})
            events.append({'venue': event.venue, 'title': event.title, 'tickets': event.tickets, 'image': event.image})
    return events
            
@app.route('/')
@app.route('/home')
def home():
    e = Event.query.order_by(Event.show_date).all()
    events = helper(e)
    lastDate = events[0]
    return render_template('home.html', events=events, lastDate=lastDate)

@app.route('/sort')
def sort():
    currentDate = datetime.now().date()
    venues = Event.query.distinct(Event.venue).with_entities(Event.venue).all()
    venues = [venue[0] for venue in venues]
    finalDate = Event.query.filter(Event.show_date >= currentDate).order_by(Event.show_date.desc()).first()
    return render_template('sort.html', venues=venues, currentDate=currentDate, finalDate=finalDate)

@app.route('/sorted')
def sorted():
    selectedVenues = request.args.getlist('venue') 
    startDate = request.args.get('start')
    endDate = request.args.get('end')
    query = Event.query
    if selectedVenues:
        query = query.filter(Event.venue.in_(selectedVenues))
    if startDate:
        query = query.filter(Event.show_date >= startDate)
    if endDate:
        query = query.filter(Event.show_date <= endDate)
    query = query.order_by(Event.show_date).all() 
    events = helper(query)
    lastDate = events[0]
    return render_template('home.html', events=events, lastDate=lastDate)

@app.route('/prune')
def prune():
    today = date.today()
    eventsToBePruned = Event.query.filter(Event.show_date < today).all()
    titles = [event.title for event in eventsToBePruned]
    for event in eventsToBePruned:
        print('pruning: ', event.title, event.show_date)
        db.session.delete(event)
    db.session.commit()
    return f'Pruned {len(eventsToBePruned)} events: {titles}'