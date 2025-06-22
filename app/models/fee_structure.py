from app import db
from datetime import datetime
from app.models.fee import Fee

class FeeStructure(db.Model):
    __tablename__ = 'fee_structures'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    academic_year = db.Column(db.String(9), nullable=False)  # e.g., "2023-2024"
    semester = db.Column(db.String(20), nullable=False)  # e.g., "First Semester"
    type = db.Column(db.String(50))  # tuition, registration, examination, etc.
    amount = db.Column(db.Float)
    due_date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = db.relationship('Course', backref=db.backref('fee_structures', lazy='dynamic'))
    generated_fees = db.relationship('Fee', back_populates='fee_structure', lazy='dynamic')
    
    def __repr__(self):
        return f'<FeeStructure {self.type}: {self.amount}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'academic_year': self.academic_year,
            'semester': self.semester,
            'type': self.type,
            'amount': self.amount,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 