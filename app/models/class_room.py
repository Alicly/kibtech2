from app import db
from datetime import datetime

# Association table for many-to-many relationship between ClassRoom and User
class_enrollments = db.Table(
    'class_enrollments',
    db.Column('student_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('class_rooms.id'), primary_key=True)
)

class ClassRoom(db.Model):
    __tablename__ = 'class_rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    day = db.Column(db.String(10), nullable=False)  # Day of the week (e.g., 'Monday', 'Tuesday')
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    course = db.relationship('Course', back_populates='classes')
    lecturer = db.relationship('User', 
                             back_populates='classes_taught',
                             foreign_keys=[lecturer_id])
    students = db.relationship('User',
                             secondary=class_enrollments,
                             back_populates='enrolled_classes',
                             lazy='dynamic')
    assignments = db.relationship('Assignment',
                                back_populates='class_room',
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    attendance_records = db.relationship('Attendance',
                                       back_populates='class_room',
                                       lazy='dynamic',
                                       cascade='all, delete-orphan')
    teaching_materials = db.relationship('TeachingMaterial',
                                       back_populates='class_room',
                                       lazy='dynamic',
                                       cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ClassRoom {self.name}>' 