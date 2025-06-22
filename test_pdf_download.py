from app import create_app, db
from app.models import User, Student, Grade
from datetime import datetime

app = create_app()

with app.app_context():
    print("=== TESTING PDF DOWNLOAD ===\n")
    
    # Check if pdfkit is available
    try:
        import pdfkit
        print("✓ pdfkit is available")
        PDFKIT_AVAILABLE = True
    except ImportError:
        print("✗ pdfkit is not available")
        PDFKIT_AVAILABLE = False
    
    # Get a student with grades
    student = Student.query.filter_by(email='student3@kitelakpelttc.edu').first()
    if not student:
        print("No student found with email student3@kitelakpelttc.edu")
        exit()
    
    print(f"Student: {student.first_name} {student.last_name}")
    print(f"Student Number: {student.student_number}")
    print(f"Course: {student.course.name if student.course else 'No course'}")
    print(f"Course ID: {student.course_id}")
    
    if not student.course:
        print("⚠️  WARNING: Student has no course assigned!")
        print("This might cause issues with the PDF generation.")
    
    # Get grades for this student
    results = Grade.query.filter_by(student_id=student.id).all()
    print(f"Number of grades: {len(results)}")
    
    for grade in results:
        print(f"  - {grade.unit.name if grade.unit else 'No unit'}: {grade.score}% ({grade.grade_letter})")
    
    # Test template rendering
    try:
        from flask import render_template
        html = render_template('student/results_pdf.html',
                              student=student,
                              results=results,
                              academic_year=str(datetime.now().year),
                              semester='First Semester',
                              current_time=datetime.now())
        print("✓ Template rendering successful")
        print(f"HTML length: {len(html)} characters")
    except Exception as e:
        print(f"✗ Template rendering failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n=== TEST COMPLETE ===") 