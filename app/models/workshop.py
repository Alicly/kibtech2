from app import db
from datetime import datetime

class Workshop(db.Model):
    __tablename__ = 'workshops'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    capacity = db.Column(db.Integer)
    status = db.Column(db.String(20))  # scheduled, ongoing, completed, cancelled
    
    # Relationships
    course = db.relationship('Course', backref='workshops')
    instructor = db.relationship('User', backref='workshops_taught')
    participants = db.relationship('User',
                                 secondary='workshop_participants',
                                 backref='workshops_attended',
                                 lazy='dynamic')

    def __repr__(self):
        return f'<Workshop {self.name}>'

# Association table for workshop participants
workshop_participants = db.Table('workshop_participants',
    db.Column('workshop_id', db.Integer, db.ForeignKey('workshops.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('registration_date', db.DateTime, nullable=False),
    db.Column('attendance_status', db.String(20))  # registered, attended, cancelled
) 