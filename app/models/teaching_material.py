from app import db
from datetime import datetime


class TeachingMaterial(db.Model):
    __tablename__ = 'teaching_materials'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(200))
    
    # Foreign Keys
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class_rooms.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    module = db.relationship('Module', back_populates='materials')
    lecturer = db.relationship('User', back_populates='teaching_materials')
    class_room = db.relationship('ClassRoom', back_populates='teaching_materials')
    
    def __repr__(self):
        return f'<TeachingMaterial {self.title}>' 