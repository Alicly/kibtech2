from app import db
from datetime import datetime

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50))  # e.g., "Technical", "Vocational"
    duration = db.Column(db.String(50))  # e.g., "2 years", "6 months"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    modules = db.relationship('Module', backref='course', lazy='dynamic')
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic')
    fee_structures = db.relationship('FeeStructure', backref='course', lazy='dynamic')
    exams = db.relationship('Exam', backref='course', lazy='dynamic')
    units = db.relationship('Unit', backref='course', lazy='dynamic')

    def __repr__(self):
        return f'<Course {self.code}>' 