#!/usr/bin/env python3
"""
Script to assign test grades to students for demonstration purposes.
This will help showcase the grading system functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Student, Course, Unit, Grade, User
import random
from datetime import datetime

def assign_test_grades():
    """Assign test grades to students for demonstration"""
    app = create_app()
    
    with app.app_context():
        print("Starting test grade assignment...")
        
        # Get all students
        students = Student.query.all()
        if not students:
            print("No students found. Please create some students first.")
            return
        
        # Get all courses with units
        courses = Course.query.all()
        if not courses:
            print("No courses found. Please create some courses first.")
            return
        
        grades_created = 0
        grades_updated = 0
        
        for student in students:
            if not student.course:
                print(f"Student {student.first_name} {student.last_name} has no course assigned. Skipping...")
                continue
            
            # Get units for this student's course
            units = student.course.units.all()
            if not units:
                print(f"No units found for course {student.course.name}. Skipping...")
                continue
            
            print(f"Processing grades for {student.first_name} {student.last_name} ({student.course.name})")
            
            for unit in units:
                # Check if grade already exists
                existing_grade = Grade.query.filter_by(student_id=student.id, unit_id=unit.id).first()
                
                if existing_grade:
                    # Update existing grade with new random score
                    score = random.uniform(50, 95)  # Random score between 50-95
                    existing_grade.score = round(score, 1)
                    existing_grade.grade_letter = get_grade_letter(score)
                    existing_grade.remarks = get_random_remark(score)
                    existing_grade.updated_at = datetime.utcnow()
                    grades_updated += 1
                    print(f"  Updated {unit.code}: {score:.1f}% ({existing_grade.grade_letter})")
                else:
                    # Create new grade
                    score = random.uniform(50, 95)  # Random score between 50-95
                    new_grade = Grade(
                        student_id=student.id,
                        unit_id=unit.id,
                        score=round(score, 1),
                        grade_letter=get_grade_letter(score),
                        remarks=get_random_remark(score)
                    )
                    db.session.add(new_grade)
                    grades_created += 1
                    print(f"  Created {unit.code}: {score:.1f}% ({new_grade.grade_letter})")
        
        try:
            db.session.commit()
            print(f"\n✅ Grade assignment completed successfully!")
            print(f"📊 Created: {grades_created} new grades")
            print(f"📝 Updated: {grades_updated} existing grades")
            print(f"📈 Total: {grades_created + grades_updated} grades processed")
            
            # Show summary
            show_grade_summary()
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error assigning grades: {str(e)}")

def get_grade_letter(score):
    """Convert numerical score to grade letter"""
    if score >= 80:
        return 'A'
    elif score >= 70:
        return 'B'
    elif score >= 60:
        return 'C'
    elif score >= 50:
        return 'D'
    else:
        return 'F'

def get_random_remark(score):
    """Get a random remark based on score"""
    if score >= 80:
        remarks = [
            "Excellent work! Keep it up!",
            "Outstanding performance!",
            "Very well done!",
            "Exceptional understanding of the material."
        ]
    elif score >= 70:
        remarks = [
            "Good work!",
            "Well done!",
            "Solid performance.",
            "Good understanding of the concepts."
        ]
    elif score >= 60:
        remarks = [
            "Satisfactory work.",
            "Average performance.",
            "Basic understanding demonstrated.",
            "Room for improvement."
        ]
    elif score >= 50:
        remarks = [
            "Below average performance.",
            "Needs improvement.",
            "Basic concepts need reinforcement.",
            "More effort required."
        ]
    else:
        remarks = [
            "Needs significant improvement.",
            "Failed to meet minimum requirements.",
            "Requires remedial work.",
            "Must retake this unit."
        ]
    
    return random.choice(remarks)

def show_grade_summary():
    """Show a summary of the grading system"""
    print("\n" + "="*60)
    print("📋 GRADING SYSTEM SUMMARY")
    print("="*60)
    
    # Get statistics
    total_students = Student.query.count()
    total_courses = Course.query.count()
    total_units = Unit.query.count()
    total_grades = Grade.query.count()
    
    # Grade distribution
    grade_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    grades = Grade.query.all()
    for grade in grades:
        if grade.grade_letter in grade_distribution:
            grade_distribution[grade.grade_letter] += 1
    
    # Calculate average score
    total_score = sum(g.score for g in grades if g.score is not None)
    average_score = total_score / len(grades) if grades else 0
    
    print(f"👥 Total Students: {total_students}")
    print(f"📚 Total Courses: {total_courses}")
    print(f"📖 Total Units: {total_units}")
    print(f"⭐ Total Grades: {total_grades}")
    print(f"📊 Average Score: {average_score:.1f}%")
    
    print("\n📈 Grade Distribution:")
    for grade, count in grade_distribution.items():
        percentage = (count / total_grades * 100) if total_grades > 0 else 0
        print(f"   {grade}: {count} ({percentage:.1f}%)")
    
    print("\n🎯 Grade Scale:")
    print("   A: 80-100% (Excellent)")
    print("   B: 70-79%  (Good)")
    print("   C: 60-69%  (Average)")
    print("   D: 50-59%  (Below Average)")
    print("   F: 0-49%   (Fail)")
    
    print("\n🚀 Next Steps:")
    print("   1. Login as a lecturer to access the grading system")
    print("   2. View and update grades for your courses")
    print("   3. Students can view their updated grades in their portal")
    print("   4. Generate grading reports and statistics")

if __name__ == "__main__":
    assign_test_grades() 