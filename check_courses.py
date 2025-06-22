from app import create_app, db
from app.models import Course, User
from datetime import datetime

def check_courses():
    app = create_app()
    with app.app_context():
        print("=== COURSE DATABASE CHECK ===\n")
        
        # Get total count of courses
        total_courses = Course.query.count()
        print(f"Total courses in database: {total_courses}")
        
        # Get courses by category
        categories = db.session.query(Course.category).distinct().all()
        print(f"\nCategories found: {len(categories)}")
        
        for category in categories:
            category_name = category[0]
            if category_name:
                course_count = Course.query.filter_by(category=category_name).count()
                print(f"  {category_name}: {course_count} courses")
        
        # List all courses with details
        print(f"\n=== ALL COURSES IN DATABASE ===")
        courses = Course.query.order_by(Course.category, Course.code).all()
        
        if not courses:
            print("No courses found in database!")
            return
        
        current_category = None
        for course in courses:
            if course.category != current_category:
                current_category = course.category
                print(f"\n--- {current_category.upper()} ---")
            
            print(f"  {course.code}: {course.name}")
            print(f"    Level: {course.level}")
            print(f"    Duration: {course.duration}")
            print(f"    Fee: KES {course.fee}")
            print(f"    Capacity: {course.capacity}")
            print(f"    Status: {'Active' if course.is_active else 'Inactive'}")
            print()
        
        # Check for expected courses from import script
        expected_courses = [
            'AEXT101', 'SARD101', 'AEXT102',  # Agriculture
            'ELE101', 'ELE102', 'ELE103', 'ELE104',  # Electrical
            'FDM101', 'FD101', 'FD102', 'TM101', 'HBT101', 'HBT102', 'HBT103',  # Fashion
            'WF101', 'WF102', 'AT101', 'AT102', 'DC101',  # Mechanical
            'BT101', 'CE101', 'PL101', 'PL102', 'BA101',  # Civil
            'FBP101', 'FP101', 'FP102',  # Hospitality
            'SCM101', 'SCM102', 'ACC101', 'BM101', 'OA101', 'OA102', 'OA103',  # Business
            'ICT101', 'ICT102', 'CP101',  # ICT
            'SW101', 'SW102',  # Liberal
            'FT101', 'FT102', 'SLT101', 'SLT102'  # Science
        ]
        
        print("=== EXPECTED COURSES CHECK ===")
        missing_courses = []
        for expected_code in expected_courses:
            course = Course.query.filter_by(code=expected_code).first()
            if course:
                print(f"✅ {expected_code}: {course.name}")
            else:
                print(f"❌ {expected_code}: MISSING")
                missing_courses.append(expected_code)
        
        if missing_courses:
            print(f"\n❌ Missing {len(missing_courses)} courses: {', '.join(missing_courses)}")
        else:
            print(f"\n✅ All expected courses are present!")
        
        # Check for any extra courses not in expected list
        extra_courses = []
        for course in courses:
            if course.code not in expected_courses:
                extra_courses.append(course.code)
        
        if extra_courses:
            print(f"\n⚠️  Extra courses found: {', '.join(extra_courses)}")
        
        # Summary
        print(f"\n=== SUMMARY ===")
        print(f"Total courses in database: {total_courses}")
        print(f"Expected courses: {len(expected_courses)}")
        print(f"Missing courses: {len(missing_courses)}")
        print(f"Extra courses: {len(extra_courses)}")
        
        if len(missing_courses) > 0:
            print(f"\nTo add missing courses, run: python import_courses.py")

if __name__ == '__main__':
    check_courses() 