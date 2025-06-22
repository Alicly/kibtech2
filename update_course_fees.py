from app import create_app, db
from app.models.course import Course
from courses_agriculture import AGRICULTURE_COURSES
from courses_electrical import ELECTRICAL_COURSES
from courses_fashion import FASHION_COURSES
from courses_mechanical import MECHANICAL_COURSES
from courses_building import BUILDING_COURSES
from courses_hospitality import HOSPITALITY_COURSES
from courses_business import BUSINESS_COURSES
from courses_computing import COMPUTING_COURSES

app = create_app()

def update_course_fees():
    with app.app_context():
        # Get all courses from the database
        courses = Course.query.all()
        
        # Create a dictionary of course names to fees from our course data
        course_fees = {}
        all_courses = []
        
        # Add courses from each department
        try:
            all_courses.extend(AGRICULTURE_COURSES)
            all_courses.extend(ELECTRICAL_COURSES)
            all_courses.extend(FASHION_COURSES)
            all_courses.extend(MECHANICAL_COURSES)
            all_courses.extend(BUILDING_COURSES)
            all_courses.extend(HOSPITALITY_COURSES)
            all_courses.extend(BUSINESS_COURSES)
            all_courses.extend(COMPUTING_COURSES)
        except Exception as e:
            print(f"Error loading course data: {str(e)}")
            return
        
        # Create fee mapping
        for course_data in all_courses:
            try:
                course_fees[course_data['name']] = course_data['fee']
            except KeyError as e:
                print(f"Error: Missing {e} in course data for {course_data.get('name', 'Unknown course')}")
                continue
        
        # Update fees in database
        updated_count = 0
        for course in courses:
            if course.name in course_fees:
                course.fee = course_fees[course.name]
                updated_count += 1
                print(f"Updated {course.name}: {course.fee} KES")
        
        try:
            db.session.commit()
            print(f"\nSuccessfully updated fees for {updated_count} courses")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating fees: {str(e)}")

if __name__ == '__main__':
    update_course_fees() 