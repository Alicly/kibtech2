from app import create_app, db
from app.models import Announcement
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Check if announcements table exists (SQLite syntax)
        result = db.session.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='announcements'
        """))
        table_exists = result.fetchone() is not None
        
        if not table_exists:
            # Create announcements table
            db.session.execute(text("""
                CREATE TABLE announcements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(200) NOT NULL,
                    content TEXT,
                    course_id INTEGER,
                    created_by INTEGER,
                    created_at DATETIME,
                    updated_at DATETIME,
                    priority VARCHAR(20) DEFAULT 'normal',
                    status VARCHAR(20) DEFAULT 'active',
                    expiry_date DATETIME,
                    FOREIGN KEY (course_id) REFERENCES courses (id),
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            """))
            db.session.commit()
            print("Created announcements table successfully")
        else:
            print("Announcements table already exists")
            
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}") 