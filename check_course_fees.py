#!/usr/bin/env python3
"""
Script to check and set course fees for testing
"""

from app import create_app, db
from app.models.course import Course

def check_and_set_course_fees():
    app = create_app()
    with app.app_context():
        # Get all courses
        courses = Course.query.all()
        
        print("Current Course Fees:")
        print("-" * 50)
        
        for course in courses:
            print(f"Course: {course.name}")
            print(f"Current Fee: KSH {course.fee if course.fee else 0}")
            
            # Set a sample fee if none exists
            if not course.fee:
                # Set different fees based on course level
                if 'certificate' in course.level.lower() if course.level else '':
                    course.fee = 25000.0
                elif 'diploma' in course.level.lower() if course.level else '':
                    course.fee = 35000.0
                else:
                    course.fee = 30000.0
                print(f"Setting fee to: KSH {course.fee}")
            print()
        
        # Commit changes
        db.session.commit()
        print("Course fees updated successfully!")
        
        # Show summary
        print("\nFee Summary:")
        print("-" * 30)
        total_fee = sum(course.fee for course in courses if course.fee)
        print(f"Total courses with fees: {len([c for c in courses if c.fee])}")
        print(f"Total fee amount: KSH {total_fee:,.2f}")

if __name__ == "__main__":
    check_and_set_course_fees() 