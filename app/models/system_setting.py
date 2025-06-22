from datetime import datetime
from app import db
 
class SystemSetting(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Text)
    setting_type = db.Column(db.String(50), default='text')  # text, image, boolean, number
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SystemSetting {self.setting_key}>'
    
    @staticmethod
    def get_setting(key, default=None):
        """Get a setting value by key"""
        setting = SystemSetting.query.filter_by(setting_key=key).first()
        return setting.setting_value if setting else default
    
    @staticmethod
    def set_setting(key, value, setting_type='text', description=None):
        """Set a setting value by key"""
        setting = SystemSetting.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = value
            setting.setting_type = setting_type
            if description:
                setting.description = description
        else:
            setting = SystemSetting(
                setting_key=key,
                setting_value=value,
                setting_type=setting_type,
                description=description
            )
            db.session.add(setting)
        db.session.commit()
        return setting 