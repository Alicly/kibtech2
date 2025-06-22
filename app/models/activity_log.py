from app import db
from datetime import datetime

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # e.g., 'login', 'assignment_submit', 'exam_taken'
    description = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', backref=db.backref('activity_logs', lazy=True))
    
    def __repr__(self):
        return f'<ActivityLog {self.activity_type} - {self.timestamp}>'
    
    @staticmethod
    def log_activity(student_id, activity_type, description=None):
        """Helper method to create a new activity log entry"""
        log = ActivityLog(
            student_id=student_id,
            activity_type=activity_type,
            description=description
        )
        db.session.add(log)
        db.session.commit()
        return log 