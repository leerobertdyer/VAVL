from flask import render_template, request, jsonify
from .models import Event
from app import app
from datetime import datetime, timedelta
from .blueprints.venues import routes


def helper(allEvents):
    lastDate = allEvents[0].show_date.date()
    today = datetime.now().date()
    i = 0
    while lastDate < today:
        i += 1
        lastDate = allEvents[i].show_date.date()
    events = []
    events.append({'newDate': lastDate.strftime('%B %-d, %Y')})

    for e in allEvents:
        if e.show_date.date() < lastDate:
            continue
        if e.show_date.date() > lastDate:
            events.append({'newDate': e.show_date.strftime('%B %-d, %Y')})
            lastDate = e.show_date.date()
        events.append({'venue': e.venue, 'title': e.title, 'tickets': e.tickets, 'image': e.image})
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

@app.route('/update-feed')
def update():
    # last_entry = Event.query.order_by(Event.created.desc()).first()
    # if last_entry is not None:
        # time_diff = datetime.now() - last_entry.created
        # twentyFourHours = 24 * 60 * 60
        # if time_diff.total_seconds() > twentyFourHours:
            # print('LAST ENTRY DATE: ', last_entry.created)
            # print('TIME DIFFERENCE: ', time_diff)
    print("Scraping data...", datetime.now())
    routes.eagle()
    routes.peel()
    routes.rabbit()
    routes.cherokee()
    routes.salvage()
    routes.eulogy()
    routes.fleetwoods()
    print("Scraping completed.", datetime.now().time())
    e = Event.query.order_by(Event.show_date).all()
    events = helper(e)
    lastDate = events[0]
    return "Database Updated"
    