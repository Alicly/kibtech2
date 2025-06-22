from app import db
from datetime import datetime

class Exam(db.Model):
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    academic_year = db.Column(db.String(9), nullable=False)  # e.g., "2023-2024"
    semester = db.Column(db.String(20), nullable=False)  # e.g., "First Semester"
    exam_date = db.Column(db.DateTime, nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)  # e.g., "Final", "Mid-term"
    total_marks = db.Column(db.Float, nullable=False)
    pass_mark = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    course = db.relationship('Course', back_populates='exams')
    module = db.relationship('Module', back_populates='exams')
    results = db.relationship('ExamResult', back_populates='exam', lazy='dynamic')
    
    def __repr__(self):
        return f'<Exam {self.exam_type} - {self.academic_year}>'

class ExamResult(db.Model):
    __tablename__ = 'exam_results'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(2))  # e.g., "A", "B+", "C"
    remarks = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = db.relationship('User', backref='exam_results')
    exam = db.relationship('Exam', back_populates='results')
    
    def __repr__(self):
        return f'<ExamResult {self.student_id} - {self.marks_obtained}>' 