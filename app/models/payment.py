from datetime import datetime
from app import db

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    fee_id = db.Column(db.Integer, db.ForeignKey('fees.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # e.g., "cash", "bank transfer"
    reference_number = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Staff who created/updated
    notes = db.Column(db.Text)  # Staff notes about the payment
    
    # Relationships
    student = db.relationship('Student', back_populates='payments')
    fee = db.relationship('Fee', back_populates='payments')
    created_by_user = db.relationship('User', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<Payment {self.id} - {self.amount}>'
    
    @property
    def status_display(self):
        """Get display status with color coding"""
        status_map = {
            'pending': 'warning',
            'completed': 'success',
            'failed': 'danger'
        }
        return status_map.get(self.status, 'secondary')
    
    @classmethod
    def get_student_payment_history(cls, student_id):
        """Get comprehensive payment history for a student"""
        payments = cls.query.filter_by(student_id=student_id).order_by(cls.payment_date.desc()).all()
        
        total_paid = sum(payment.amount for payment in payments if payment.status == 'completed')
        recent_payments = payments[:10]  # Last 10 payments
        
        return {
            'payments': payments,
            'recent_payments': recent_payments,
            'total_paid': total_paid
        } 