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

# Combine all courses into a department-wise dictionary
courses = {
    "AGRICULTURE & ENVIRONMENTAL STUDIES": AGRICULTURE_COURSES,
    "ELECTRICAL & ELECTRONICS ENGINEERING": ELECTRICAL_COURSES,
    "FASHION DESIGN & COSMETOLOGY": FASHION_COURSES,
    "MECHANICAL & AUTOMOTIVE ENGINEERING": MECHANICAL_COURSES,
    "BUILDING & CIVIL ENGINEERING": BUILDING_COURSES,
    "HOSPITALITY & INSTITUTIONAL MANAGEMENT": HOSPITALITY_COURSES,
    "BUSINESS STUDIES": BUSINESS_COURSES,
    "COMPUTING & INFORMATICS": COMPUTING_COURSES
}

def generate_course_code(name, level):
    """Generate a unique course code based on name and level."""
    # Take first letter of each word in name (up to 3 letters)
    name_code = ''.join(word[0].upper() for word in name.split()[:3])
    # Add level code
    level_code = ''.join(word[0].upper() for word in level.split()[:2])
    # Add a timestamp to ensure uniqueness
    from datetime import datetime
    timestamp = datetime.now().strftime('%y%m')
    return f"{name_code}{level_code}{timestamp}"

def add_courses():
    with app.app_context():
        for department, dept_courses in courses.items():
            print(f"\nAdding courses for {department}:")
            for course_data in dept_courses:
                # Generate a unique course code
                code = generate_course_code(course_data['name'], course_data['level'])
                
                # Create course description
                description = f"{course_data['name']} - {course_data['level']}\n"
                description += f"Duration: {course_data['duration']}\n"
                description += f"Entry Requirements: {course_data['entry_requirements']}\n"
                description += f"Examining Body: {course_data['exam_body']}"
                
                # Check if course already exists
                existing_course = Course.query.filter_by(name=course_data['name'], 
                                                       level=course_data['level']).first()
                if existing_course:
                    print(f"Course already exists: {course_data['name']} ({course_data['level']})")
                    continue
                
                # Create new course
                course = Course(
                    code=code,
                    name=course_data['name'],
                    description=description,
                    duration=course_data['duration'],
                    level=course_data['level'],
                    category=course_data['category'],
                    entry_requirements=course_data['entry_requirements'],
                    exam_body=course_data['exam_body'],
                    is_active=True
                )
                
                try:
                    db.session.add(course)
                    db.session.commit()
                    print(f"Added: {course_data['name']} ({course_data['level']})")
                except Exception as e:
                    db.session.rollback()
                    print(f"Error adding {course_data['name']}: {str(e)}")

if __name__ == '__main__':
    add_courses()