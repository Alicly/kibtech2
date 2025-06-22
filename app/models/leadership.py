from datetime import datetime
from app import db

class LeadershipTeam(db.Model):
    __tablename__ = 'leadership_teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    order = db.Column(db.Integer, default=0)  # For sorting/ordering team members
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<LeadershipTeam {self.name}: {self.position}>' 