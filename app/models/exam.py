from datetime import datetime
from app import db

class Exam(db.Model):
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    exam_type = db.Column(db.String(50))  # e.g., "Midterm", "Final", "Quiz"
    total_marks = db.Column(db.Float)
    passing_marks = db.Column(db.Float)
    duration = db.Column(db.Integer)  # Duration in minutes
    exam_date = db.Column(db.DateTime)
    venue = db.Column(db.String(100))
    status = db.Column(db.String(20), default='scheduled')  # scheduled, ongoing, completed, cancelled
    academic_year = db.Column(db.String(20))  # e.g., "2023/2024"
    semester = db.Column(db.String(20))  # e.g., "First", "Second", "Third"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    
    # Relationships
    module = db.relationship('Module', back_populates='exams')
    results = db.relationship('ExamResult', back_populates='exam', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Exam {self.title}>'

class ExamResult(db.Model):
    __tablename__ = 'exam_results'
    
    id = db.Column(db.Integer, primary_key=True)
    marks_obtained = db.Column(db.Float)
    grade = db.Column(db.String(2))
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    
    # Relationships
    exam = db.relationship('Exam', back_populates='results')
    student = db.relationship('Student', back_populates='exam_results')
    module = db.relationship('Module', back_populates='exam_results')
    
    def __repr__(self):
        return f'<ExamResult {self.student_id} - {self.exam_id}>' 