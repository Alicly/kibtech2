print("Starting student-course sync...")

from app import create_app, db
from app.models.student import Student
from app.models.course import Course

app = create_app()
with app.app_context():
    try:
        students = Student.query.filter(Student.course_id.isnot(None)).all()
        print(f"Found {len(students)} students with a course_id.")
        count = 0
        for student in students:
            print(f"Checking student {student.id} ({student.student_number}) with course_id {student.course_id}")
            course = Course.query.get(student.course_id)
            if course:
                print(f"  Found course {course.id} ({course.name})")
                if course not in student.enrolled_courses:
                    student.enrolled_courses.append(course)
                    print(f"  Added student {student.id} to course {course.id}")
                    count += 1
                else:
                    print(f"  Student {student.id} already enrolled in course {course.id}")
            else:
                print(f"  Course with id {student.course_id} not found!")
        db.session.commit()
        print(f"Synced {count} students to their courses.")
    except Exception as e:
        print(f"Error occurred: {e}")