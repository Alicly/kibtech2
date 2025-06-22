from app import db
from datetime import datetime
from app.models.enrollment import student_course_enrollments

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(200))
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, inactive, graduated, suspended
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('student', uselist=False), foreign_keys=[email], primaryjoin='Student.email == User.email')
    course = db.relationship('Course', back_populates='students')
    enrollments = db.relationship('Enrollment', back_populates='student', lazy='dynamic', cascade='all, delete-orphan')
    enrolled_courses = db.relationship('Course',
                                     secondary=student_course_enrollments,
                                     back_populates='students',
                                     lazy='dynamic')
    grades = db.relationship('Grade', back_populates='student', lazy='dynamic')
    attendance_records = db.relationship('Attendance', back_populates='student', lazy='dynamic')
    exam_results = db.relationship('ExamResult', back_populates='student', lazy='dynamic')
    unit_registrations = db.relationship('UnitRegistration', back_populates='student', lazy='dynamic')
    fees = db.relationship('Fee', back_populates='student', lazy='dynamic')
    payments = db.relationship('Payment', back_populates='student', lazy='dynamic')
    submissions = db.relationship('AssignmentSubmission', back_populates='student', lazy='dynamic')
    
    def __repr__(self):
        return f'<Student {self.student_number}: {self.first_name} {self.last_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_number': self.student_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'address': self.address,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'status': self.status,
            'course_id': self.course_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 