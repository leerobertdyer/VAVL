from app import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    show_date = db.Column(db.DateTime)
    tickets = db.Column(db.String)
    cost = db.Column(db.String)
    image = db.Column(db.String)
    link = db.Column(db.String)
    