from app.extensions import db
from datetime import datetime

class Tool(db.Model):
    __tablename__ = 'tool'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tool_type = db.Column(db.String(50))  # Hand Tool, Power Tool, Equipment
    category = db.Column(db.String(50))  # Electrical, Plumbing, Construction, etc.
    description = db.Column(db.Text)
    manufacturer = db.Column(db.String(100))
    model_number = db.Column(db.String(50))
    serial_number = db.Column(db.String(50), unique=True)
    purchase_date = db.Column(db.Date)
    condition = db.Column(db.String(20))  # New, Good, Fair, Poor
    location = db.Column(db.String(100))  # Storage location
    maintenance_schedule = db.Column(db.Text)
    last_maintenance = db.Column(db.Date)
    next_maintenance = db.Column(db.Date)
    safety_instructions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships - Commented out problematic relationships for now
    # maintenance_records = db.relationship('MaintenanceRecord', backref='tool', lazy=True)
    # usage_records = db.relationship('ToolUsage', backref='tool', lazy=True)

    def __repr__(self):
        return f'<Tool {self.name}>' 