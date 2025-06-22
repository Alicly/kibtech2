from datetime import datetime
from app import db

class News(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(200))
    is_published = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<News {self.title}>' 