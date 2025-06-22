from app import create_app, db
from app.models import Course

def simple_check():
    app = create_app()
    with app.app_context():
        try:
            # Test database connection
            print("Testing database connection...")
            db.engine.execute("SELECT 1")
            print("✅ Database connection successful!")
            
            # Check if courses table exists
            print("\nChecking if courses table exists...")
            result = db.engine.execute("SELECT COUNT(*) FROM courses")
            count = result.fetchone()[0]
            print(f"✅ Courses table exists with {count} records")
            
            # List first 5 courses
            print("\nFirst 5 courses in database:")
            courses = Course.query.limit(5).all()
            for course in courses:
                print(f"  {course.code}: {course.name}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    simple_check() 