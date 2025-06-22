from app.extensions import db
from datetime import datetime

class MaintenanceRecord(db.Model):
    __tablename__ = 'maintenance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    performed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    maintenance_type = db.Column(db.String(50))  # routine, repair, calibration
    description = db.Column(db.Text)
    date_performed = db.Column(db.DateTime, default=datetime.utcnow)
    next_maintenance_date = db.Column(db.DateTime)
    cost = db.Column(db.Float)
    status = db.Column(db.String(20))  # completed, pending, scheduled
    
    # Relationships - Temporarily commented out to fix initialization
    # equipment = db.relationship('Equipment', backref='maintenance_records')
    # technician = db.relationship('User', backref='maintenance_performed')

    def __repr__(self):
        return f'<MaintenanceRecord {self.id}>'

class ToolUsage(db.Model):
    __tablename__ = 'tool_usage'
    
    id = db.Column(db.Integer, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workshop_id = db.Column(db.Integer, db.ForeignKey('workshop.id'))
    check_out_time = db.Column(db.DateTime, nullable=False)
    check_in_time = db.Column(db.DateTime)
    condition_before = db.Column(db.String(20))
    condition_after = db.Column(db.String(20))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships - Temporarily commented out to fix initialization
    # tool = db.relationship('Tool', backref='usage_records', lazy=True)
    # user = db.relationship('User', backref='tool_usage_records', lazy=True)
    # workshop = db.relationship('Workshop', backref='tool_usage_records', lazy=True)

    def __repr__(self):
        return f'<ToolUsage {self.id}>'

class MaintenanceRequest(db.Model):
    __tablename__ = 'maintenance_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    request_type = db.Column(db.String(50))  # repair, maintenance, inspection
    description = db.Column(db.Text)
    priority = db.Column(db.String(20))  # low, medium, high, urgent
    status = db.Column(db.String(20))  # pending, approved, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - Temporarily commented out to fix initialization
    # equipment = db.relationship('Equipment', backref='maintenance_requests')
    # requester = db.relationship('User', backref='maintenance_requests')

# Remove or comment out any SystemSetting model in this file to avoid duplicate table definition errors.
# class SystemSetting(db.Model):
#     __tablename__ = 'system_settings'
#     id = db.Column(db.Integer, primary_key=True)
#     key = db.Column(db.String(64), unique=True, nullable=False)
#     
#     @staticmethod
#     def get(key, default=None):
#         setting = SystemSetting.query.filter_by(key=key).first()
#         return setting.value if setting else default
#     
#     @staticmethod
#     def set(key, value):
#         setting = SystemSetting.query.filter_by(key=key).first()
#         if not setting:
#             setting = SystemSetting(key=key, value=value)
#             db.session.add(setting)
#         else:
#             setting.value = value
#         db.session.commit() 