from app import db
from datetime import datetime

class FeeStructure(db.Model):
    __tablename__ = 'fee_structures'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    academic_year = db.Column(db.String(9), nullable=False)  # e.g., "2023-2024"
    semester = db.Column(db.String(20), nullable=False)  # e.g., "First Semester"
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    course = db.relationship('Course', back_populates='fee_structures')
    payments = db.relationship('FeePayment', back_populates='fee_structure', lazy='dynamic')
    
    def __repr__(self):
        return f'<FeeStructure {self.course_id} - {self.academic_year}>'

class FeePayment(db.Model):
    __tablename__ = 'fee_payments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fee_structure_id = db.Column(db.Integer, db.ForeignKey('fee_structures.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # e.g., "Cash", "Bank Transfer"
    reference_number = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Pending')  # Pending, Completed, Failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = db.relationship('User', backref='fee_payments')
    fee_structure = db.relationship('FeeStructure', back_populates='payments')
    
    def __repr__(self):
        return f'<FeePayment {self.student_id} - {self.amount_paid}>' 