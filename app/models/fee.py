from datetime import datetime
from app import db
from app.models.payment import Payment

# Correctly import FeeStructure
# from app.models.fee_structure import FeeStructure


class Fee(db.Model):
    __tablename__ = 'fees'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    fee_structure_id = db.Column(db.Integer, db.ForeignKey('fee_structures.id'), nullable=True)
    academic_year = db.Column(db.String(9), nullable=False)  # e.g., "2023-2024"
    semester = db.Column(db.String(20), nullable=False)  # e.g., "First Semester"
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue, partial
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Staff who updated
    notes = db.Column(db.Text)  # Staff notes about the fee
    
    # Relationships
    student = db.relationship('Student', back_populates='fees')
    fee_structure = db.relationship('FeeStructure', back_populates='generated_fees')
    payments = db.relationship(Payment, 
                             back_populates='fee', 
                             lazy='dynamic',
                             cascade='all, delete-orphan')
    updated_by_user = db.relationship('User', foreign_keys=[updated_by])
    
    def __repr__(self):
        return f'<Fee {self.student_id} - {self.academic_year}>'
    
    @property
    def total_paid(self):
        """Calculate total amount paid for this fee"""
        return sum(payment.amount for payment in self.payments.filter_by(status='completed'))
    
    @property
    def balance(self):
        """Calculate remaining balance"""
        return self.amount - self.total_paid
    
    @property
    def payment_percentage(self):
        """Calculate payment percentage"""
        if self.amount == 0:
            return 100
        return (self.total_paid / self.amount) * 100
    
    @property
    def is_overdue(self):
        """Check if fee is overdue"""
        return datetime.now().date() > self.due_date and self.balance > 0
    
    @property
    def status_display(self):
        """Get display status based on balance and due date"""
        if self.balance <= 0:
            return 'paid'
        elif self.is_overdue:
            return 'overdue'
        elif self.total_paid > 0:
            return 'partial'
        else:
            return 'pending'
    
    def update_status(self):
        """Update status based on current balance and due date"""
        self.status = self.status_display
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def get_student_fees_summary(cls, student_id):
        """Get comprehensive fee summary for a student"""
        fees = cls.query.filter_by(student_id=student_id).all()
        
        total_amount = sum(fee.amount for fee in fees)
        total_paid = sum(fee.total_paid for fee in fees)
        total_balance = sum(fee.balance for fee in fees)
        overdue_fees = [fee for fee in fees if fee.is_overdue]
        
        return {
            'total_amount': total_amount,
            'total_paid': total_paid,
            'total_balance': total_balance,
            'overdue_fees': overdue_fees,
            'fees': fees
        } 