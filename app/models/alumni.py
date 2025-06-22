from datetime import datetime
from app import db

class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    graduation_year = db.Column(db.String(10))
    course = db.Column(db.String(100))
    testimonial = db.Column(db.Text)
    photo_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Alumni {self.name}>' 