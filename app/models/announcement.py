from datetime import datetime
from app import db

class Announcement(db.Model):
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    priority = db.Column(db.String(20), default='normal')  # high, normal, low
    status = db.Column(db.String(20), default='active')  # active, archived
    expiry_date = db.Column(db.DateTime)
    
    # Relationships
    course = db.relationship('Course', backref='announcements')
    creator = db.relationship('User', backref='announcements')
    
    def __repr__(self):
        return f'<Announcement {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'course_id': self.course_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'priority': self.priority,
            'status': self.status,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None
        } 