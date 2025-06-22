from datetime import datetime
from app import db

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class_rooms.id'))
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20))  # present, absent, late, excused
    remarks = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', back_populates='attendance_records')
    class_room = db.relationship('ClassRoom', back_populates='attendance_records')

    def __repr__(self):
        return f'<Attendance {self.date}>' 