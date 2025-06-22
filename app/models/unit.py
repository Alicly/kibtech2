from app import db
from datetime import datetime

class Unit(db.Model):
    __tablename__ = 'units'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    # Relationships
    course = db.relationship('Course', back_populates='units')
    registrations = db.relationship('UnitRegistration', 
                                  back_populates='unit', 
                                  lazy='dynamic',
                                  cascade='all, delete-orphan')
    grades = db.relationship('Grade', 
                           back_populates='unit', 
                           lazy='dynamic',
                           cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', 
                                back_populates='unit', 
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    
    __table_args__ = (
        db.UniqueConstraint('code', 'course_id', name='uq_code_course'),
    )
    
    def __repr__(self):
        return f'<Unit {self.code}: {self.name}>' 