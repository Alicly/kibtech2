from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager

# Association table for many-to-many relationship between lecturers and courses
lecturer_courses = db.Table(
    'lecturer_courses',
    db.Column('lecturer_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=False)
    
    # Student specific fields
    registration_number = db.Column(db.String(20), unique=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    
    # Lecturer specific fields
    lecturer_id = db.Column(db.String(20), unique=True)
    department = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    
    # Staff specific fields
    staff_id = db.Column(db.String(20), unique=True)
    position = db.Column(db.String(100))

    # Relationships
    classes_taught = db.relationship('ClassRoom', 
                                   back_populates='lecturer', 
                                   foreign_keys='ClassRoom.lecturer_id', 
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')
    notifications = db.relationship('Notification',
                                  backref='user',
                                  lazy='dynamic',
                                  cascade='all, delete-orphan')
    enrolled_classes = db.relationship('ClassRoom',
                                     secondary='class_enrollments',
                                     back_populates='students',
                                     lazy='dynamic')
    created_assignments = db.relationship('Assignment',
                                        back_populates='lecturer',
                                        lazy='dynamic',
                                        cascade='all, delete-orphan')
    modules_taught = db.relationship('Module',
                                   back_populates='lecturer',
                                   lazy='dynamic')
    courses_taught = db.relationship(
        'Course',
        back_populates='lecturer',
        foreign_keys='Course.lecturer_id'
    )
    teaching_materials = db.relationship('TeachingMaterial',
                                       back_populates='lecturer',
                                       lazy='dynamic',
                                       cascade='all, delete-orphan')
    course = db.relationship('Course', backref='users', foreign_keys=[course_id])
    
    # Many-to-many: courses this lecturer teaches
    courses_teaching = db.relationship(
        'Course',
        secondary=lecturer_courses,
        back_populates='lecturers',
        lazy='dynamic'
    )
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 