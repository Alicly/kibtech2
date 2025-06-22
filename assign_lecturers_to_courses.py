#!/usr/bin/env python3
"""
Script to assign lecturers to courses so they can view their teaching areas and units.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Course, User

def assign_lecturers_to_courses():
    """Assign lecturers to courses"""
    app = create_app()
    
    with app.app_context():
        # Get all lecturers
        lecturers = User.query.filter_by(role='lecturer').all()
        print(f"Found {len(lecturers)} lecturers")
        
        # Get all courses
        courses = Course.query.all()
        print(f"Found {len(courses)} courses")
        
        if not lecturers:
            print("No lecturers found. Please create some lecturers first.")
            return
        
        if not courses:
            print("No courses found. Please create some courses first.")
            return
        
        # Assign lecturers to courses based on categories
        assignments_made = 0
        
        for i, course in enumerate(courses):
            # Assign lecturer based on course index (round-robin)
            lecturer = lecturers[i % len(lecturers)]
            
            # Update course with lecturer
            course.lecturer_id = lecturer.id
            assignments_made += 1
            
            print(f"Assigned {lecturer.first_name} {lecturer.last_name} to {course.code} - {course.name}")
        
        # Commit changes
        try:
            db.session.commit()
            print(f"\nSuccessfully assigned {assignments_made} courses to lecturers!")
            
            # Show summary
            print("\n" + "="*60)
            print("LECTURER ASSIGNMENT SUMMARY")
            print("="*60)
            
            for lecturer in lecturers:
                assigned_courses = Course.query.filter_by(lecturer_id=lecturer.id).all()
                total_units = sum(len(course.units.all()) for course in assigned_courses)
                
                print(f"\n📚 {lecturer.first_name} {lecturer.last_name}")
                print(f"   Courses: {len(assigned_courses)}")
                print(f"   Units: {total_units}")
                
                if assigned_courses:
                    print("   Teaching:")
                    for course in assigned_courses:
                        unit_count = len(course.units.all())
                        print(f"     • {course.code} - {course.name} ({unit_count} units)")
                else:
                    print("   No courses assigned")
            
            print("\n" + "="*60)
            print("✅ LECTURER ASSIGNMENT COMPLETED!")
            print("Lecturers can now view their courses and units in the lecturer portal.")
            print("="*60)
            
        except Exception as e:
            print(f"Error committing assignments: {e}")
            db.session.rollback()

if __name__ == '__main__':
    assign_lecturers_to_courses() 