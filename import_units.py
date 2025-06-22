#!/usr/bin/env python3
"""
Script to import units for all courses in the TVET system.
This script will create units for each course based on the Kenyan TVET curriculum.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Course, Unit
from app.data.units import create_units

def import_units():
    """Import units for all courses"""
    app = create_app()
    
    with app.app_context():
        # Get all courses
        courses = Course.query.all()
        print(f"Found {len(courses)} courses in the database")
        
        # Get units data
        units_data = create_units()
        
        total_units_created = 0
        
        for course in courses:
            print(f"\nProcessing course: {course.code} - {course.name}")
            
            # Check if units already exist for this course
            existing_units = Unit.query.filter_by(course_id=course.id).count()
            if existing_units > 0:
                print(f"  Skipping - {existing_units} units already exist")
                continue
            
            # Get units for this course
            course_units = units_data.get(course.code, [])
            
            if not course_units:
                print(f"  No units defined for course {course.code}")
                continue
            
            # Create units for this course
            units_created = 0
            for unit_data in course_units:
                try:
                    unit = Unit(
                        code=unit_data['code'],
                        name=unit_data['name'],
                        description=unit_data['description'],
                        credits=unit_data['credits'],
                        course_id=course.id
                    )
                    db.session.add(unit)
                    units_created += 1
                except Exception as e:
                    print(f"  Error creating unit {unit_data['code']}: {e}")
                    db.session.rollback()
                    continue
            
            # Commit units for this course
            try:
                db.session.commit()
                print(f"  Created {units_created} units for {course.code}")
                total_units_created += units_created
            except Exception as e:
                print(f"  Error committing units for {course.code}: {e}")
                db.session.rollback()
        
        print(f"\nTotal units created: {total_units_created}")
        print("Unit import completed!")

if __name__ == '__main__':
    import_units() 