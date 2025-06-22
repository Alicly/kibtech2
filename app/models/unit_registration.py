from datetime import datetime
from app import db

class UnitRegistration(db.Model):
    __tablename__ = 'unit_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    academic_year = db.Column(db.String(9), nullable=False)  # e.g., "2023-2024"
    semester = db.Column(db.String(20), nullable=False)  # e.g., "First Semester"
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, completed, dropped
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approval_date = db.Column(db.DateTime)
    remarks = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', back_populates='unit_registrations')
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_registrations')
    unit = db.relationship('Unit', back_populates='registrations')
    
    def __repr__(self):
        return f'<UnitRegistration {self.id}: {self.student_id} - {self.unit_id}>'

class RegistrationPeriod(db.Model):
    __tablename__ = 'registration_periods'
    
    id = db.Column(db.Integer, primary_key=True)
    academic_year = db.Column(db.String(9), nullable=False)  # e.g., "2023-2024"
    semester = db.Column(db.String(20), nullable=False)  # e.g., "First Semester"
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='created_registration_periods')
    
    def __repr__(self):
        return f'<RegistrationPeriod {self.academic_year} - {self.semester}>'
    
    @property
    def is_current(self):
        """Check if the registration period is currently active"""
        now = datetime.utcnow()
        return self.is_active and self.start_date <= now <= self.end_date 