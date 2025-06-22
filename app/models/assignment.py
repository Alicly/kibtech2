from datetime import datetime
from app import db
from app.models.assignment_submission import AssignmentSubmission

class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=False)
    total_marks = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20))  # pending, submitted, graded
    submission_date = db.Column(db.DateTime)
    grade = db.Column(db.Float)
    feedback = db.Column(db.Text)
    
    # Foreign Keys
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class_rooms.id'), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    unit = db.relationship('Unit', back_populates='assignments')
    class_room = db.relationship('ClassRoom', back_populates='assignments')
    lecturer = db.relationship('User', back_populates='created_assignments')
    submissions = db.relationship(AssignmentSubmission, 
                                back_populates='assignment', 
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    grades = db.relationship('Grade',
                           back_populates='assignment',
                           lazy='dynamic',
                           cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Assignment {self.id}: {self.title}>' 