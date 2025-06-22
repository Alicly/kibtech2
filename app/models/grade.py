from datetime import datetime
from app import db

class Grade(db.Model):
    __tablename__ = 'grades'
    
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float, nullable=False)
    grade_letter = db.Column(db.String(2))  # A, B, C, D, F
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    
    # Relationships
    student = db.relationship('Student', back_populates='grades')
    unit = db.relationship('Unit', back_populates='grades')
    assignment = db.relationship('Assignment', back_populates='grades')
    
    def __repr__(self):
        return f'<Grade {self.id}: {self.student_id} - {self.unit_id} - {self.grade_letter}>' 