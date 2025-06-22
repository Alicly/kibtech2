from datetime import datetime
from app import db

class SlideshowSlide(db.Model):
    __tablename__ = 'slideshow_slides'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    order = db.Column(db.Integer, default=0)  # For ordering slides
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SlideshowSlide {self.title}>'
    
    @classmethod
    def get_active_slides(cls):
        """Get all active slides ordered by their order field"""
        return cls.query.filter_by(is_active=True).order_by(cls.order.asc()).all()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'order': self.order,
            'is_active': self.is_active
        } 