from datetime import datetime
from app import db

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.DateTime, nullable=False)  # Time of the event
    category = db.Column(db.String(50))  # workshop, seminar, conference, graduation, other
    location = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    status = db.Column(db.String(20), default='upcoming')  # upcoming, ongoing, completed, cancelled
    registration_required = db.Column(db.Boolean, default=False)
    max_participants = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Event {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'time': self.time.isoformat() if self.time else None,
            'category': self.category,
            'location': self.location,
            'image_url': self.image_url,
            'status': self.status,
            'registration_required': self.registration_required,
            'max_participants': self.max_participants,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 