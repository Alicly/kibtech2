from datetime import datetime
from app import db

class ClassSchedule(db.Model):
    __tablename__ = 'class_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class_rooms.id'), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    day_of_week = db.Column(db.String(10))  # Monday, Tuesday, etc.
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    class_room = db.relationship('ClassRoom', backref='schedules')
    lecturer = db.relationship('User', backref='teaching_schedules') 