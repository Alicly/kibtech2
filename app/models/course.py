from app import db
from datetime import datetime
from app.models.enrollment import student_course_enrollments

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.String(50))  # e.g., "6 months", "1 year"
    level = db.Column(db.String(50))  # e.g., "Certificate", "Diploma"
    category = db.Column(db.String(50))  # e.g., "ICT", "Carpentry", "Automotive"
    capacity = db.Column(db.Integer)
    fee = db.Column(db.Float)
    image_url = db.Column(db.String(255))  # URL for course image
    student_count = db.Column(db.Integer, default=0)  # Number of enrolled students
    lecturer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    entry_requirements = db.Column(db.String(200))  # Entry requirements for the course
    exam_body = db.Column(db.String(50))  # Examining body (e.g., TVET-CDACC)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    lecturer = db.relationship('User', back_populates='courses_taught', foreign_keys=[lecturer_id])
    modules = db.relationship('Module', back_populates='course', lazy='dynamic', cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', back_populates='course', lazy='dynamic', cascade='all, delete-orphan')
    students = db.relationship('Student', 
                             secondary=student_course_enrollments,
                             back_populates='enrolled_courses',
                             lazy='dynamic')
    units = db.relationship('Unit', back_populates='course', lazy='dynamic')
    classes = db.relationship('ClassRoom', 
                            back_populates='course', 
                            lazy='dynamic', 
                            cascade='all, delete-orphan')
    # Many-to-many: lecturers teaching this course
    lecturers = db.relationship(
        'User',
        secondary='lecturer_courses',
        back_populates='courses_teaching',
        lazy='dynamic'
    )
    
    @property
    def safe_fee(self):
        """Return the fee amount, defaulting to 0 if None"""
        return self.fee if self.fee is not None else 0
    
    def __repr__(self):
        return f'<Course {self.code}: {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'duration': self.duration,
            'level': self.level,
            'category': self.category,
            'capacity': self.capacity,
            'fee': self.fee,
            'lecturer_id': self.lecturer_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 