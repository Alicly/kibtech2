from datetime import datetime
from app import db

class Assessment(db.Model):
    __tablename__ = 'assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_type = db.Column(db.String(50))  # quiz, exam, project, presentation
    description = db.Column(db.Text)
    total_marks = db.Column(db.Float)
    passing_marks = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # in minutes
    status = db.Column(db.String(20))  # draft, published, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = db.relationship('Course', backref='assessments')
    instructor = db.relationship('User', backref='created_assessments')
    submissions = db.relationship('AssessmentSubmission', backref='assessment', lazy='dynamic')

    def __repr__(self):
        return f'<Assessment {self.title}>'

class AssessmentSubmission(db.Model):
    __tablename__ = 'assessment_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    marks_obtained = db.Column(db.Float)
    feedback = db.Column(db.Text)
    status = db.Column(db.String(20))  # submitted, graded, late
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = db.relationship('User', backref='assessment_submissions')

    def __repr__(self):
        return f'<AssessmentSubmission {self.id}>' 