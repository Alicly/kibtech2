from app import db
from datetime import datetime

class Module(db.Model):
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer)
    semester = db.Column(db.String(20))
    level = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    course = db.relationship('Course', back_populates='modules')
    lecturer = db.relationship('User', back_populates='modules_taught')
    exams = db.relationship('Exam', back_populates='module', lazy='dynamic', cascade='all, delete-orphan')
    materials = db.relationship('TeachingMaterial', back_populates='module', lazy='dynamic', cascade='all, delete-orphan')
    exam_results = db.relationship('ExamResult', 
                                 back_populates='module',
                                 lazy='dynamic',
                                 primaryjoin='Module.id==ExamResult.module_id')
    
    def __repr__(self):
        return f'<Module {self.code}: {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'credits': self.credits,
            'course_id': self.course_id,
            'semester': self.semester,
            'level': self.level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 