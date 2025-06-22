from app import db
from datetime import datetime

class AssignmentSubmission(db.Model):
    __tablename__ = 'assignment_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(255))
    comments = db.Column(db.Text)
    marks_obtained = db.Column(db.Float)
    feedback = db.Column(db.Text)
    status = db.Column(db.String(20), default='submitted')  # submitted, graded, late
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    
    # Relationships
    assignment = db.relationship('Assignment', back_populates='submissions')
    student = db.relationship('Student', back_populates='submissions')
    
    def __repr__(self):
        return f'<AssignmentSubmission {self.id}: {self.student_id} - {self.assignment_id}>' 