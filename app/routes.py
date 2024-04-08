from flask import render_template, request, jsonify
from .models import Event
from app import app
from datetime import datetime

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

@app.route('/next-events')
def nextEvents():
    page = request.args.get('page', 2, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_events = Event.query.order_by(Event.show_date).paginate(page=page, per_page=per_page, error_out=False)
    events = helper(paginated_events.items)
    return jsonify({'events': events, 'has_next': paginated_events.has_next})
            
@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 2, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    e = Event.query.order_by(Event.show_date).paginate(page=page, per_page=per_page, error_out=False).items
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