#!/usr/bin/env python3
"""
Create test users for TVET Management System
This script creates default users for testing and initial setup
"""

from app import create_app, db
from app.models.user import User
from app.models.course import Course
from app.models.student import Student
import os

def create_admin_user():
    """Create admin user"""
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@tvet.ac.ke',
            first_name='System',
            last_name='Administrator',
            role='admin',
            phone='+254700000000'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("✅ Admin user created")
        return admin
    else:
        print("ℹ️ Admin user already exists")
        return admin

def create_test_courses():
    """Create some test courses"""
    courses_data = [
        {
            'name': 'Computer Science',
            'code': 'CS101',
            'description': 'Introduction to Computer Science',
            'duration': '2 years',
            'fee': 25000
        },
        {
            'name': 'Business Administration',
            'code': 'BA101',
            'description': 'Business Administration and Management',
            'duration': '2 years',
            'fee': 22000
        },
        {
            'name': 'Engineering',
            'code': 'ENG101',
            'description': 'General Engineering',
            'duration': '3 years',
            'fee': 30000
        }
    ]
    
    created_courses = []
    for course_data in courses_data:
        course = Course.query.filter_by(code=course_data['code']).first()
        if not course:
            course = Course(**course_data)
            db.session.add(course)
            created_courses.append(course)
            print(f"✅ Course created: {course.name}")
        else:
            created_courses.append(course)
            print(f"ℹ️ Course already exists: {course.name}")
    
    return created_courses

def create_test_users():
    """Create test users for different roles"""
    users_data = [
        {
            'username': 'lecturer1',
            'email': 'lecturer1@tvet.ac.ke',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'lecturer',
            'phone': '+254700000001',
            'employee_id': 'EMP001',
            'specialization': 'Computer Science'
        },
        {
            'username': 'staff1',
            'email': 'staff1@tvet.ac.ke',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'staff',
            'phone': '+254700000002',
            'employee_id': 'STAFF001',
            'position': 'Administrative Assistant'
        },
        {
            'username': 'student1',
            'email': 'student1@tvet.ac.ke',
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'role': 'student',
            'phone': '+254700000003',
            'registration_number': 'STU001',
            'gender': 'Female'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        user = User.query.filter_by(username=user_data['username']).first()
        if not user:
            user = User(**user_data)
            user.set_password('password123')
            db.session.add(user)
            created_users.append(user)
            print(f"✅ User created: {user.username} ({user.role})")
        else:
            created_users.append(user)
            print(f"ℹ️ User already exists: {user.username}")
    
    return created_users

def main():
    """Main function to create all test data"""
    app = create_app()
    
    with app.app_context():
        print("🚀 Creating test data for TVET Management System")
        print("=" * 50)
        
        try:
            # Create admin user
            admin = create_admin_user()
            
            # Create test courses
            courses = create_test_courses()
            
            # Create test users
            users = create_test_users()
            
            # Commit all changes
            db.session.commit()
            
            print("\n🎉 Test data created successfully!")
            print("\n📋 Default Login Credentials:")
            print("Admin:")
            print("  Username: admin")
            print("  Password: admin123")
            print("  Email: admin@tvet.ac.ke")
            print("\nOther Users:")
            print("  Username: lecturer1, staff1, student1")
            print("  Password: password123")
            print("\n🔐 IMPORTANT: Change these passwords after first login!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating test data: {str(e)}")
            raise

if __name__ == "__main__":
    main() 