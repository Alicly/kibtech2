from app import create_app, db
from app.models.user import User
from app.models.course import Course
from app.models.student import Student
from app.models.class_room import ClassRoom
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
app = create_app()

    with app.app_context():
        # Drop all tables and recreate them
        print("Dropping all existing tables...")
        db.drop_all()
        
        print("Creating all tables...")
        db.create_all()
        
        print("Creating sample data...")
        
        # Create sample courses
        course1 = Course(
            code='ICT001',
            name='Information Technology',
            description='Comprehensive IT course covering programming, networking, and system administration',
            duration='2 years',
            level='Diploma',
            category='ICT',
            capacity=30,
            fee=25000.0,
            entry_requirements='KCSE C- or equivalent',
            exam_body='TVET-CDACC',
            is_active=True
        )
        
        course2 = Course(
            code='ENG002',
            name='Electrical Engineering',
            description='Electrical engineering principles and practical applications',
            duration='3 years',
            level='Diploma',
            category='Engineering',
            capacity=25,
            fee=30000.0,
            entry_requirements='KCSE C or equivalent',
            exam_body='TVET-CDACC',
            is_active=True
        )
        
        db.session.add(course1)
        db.session.add(course2)
        db.session.commit()

        # Create admin user
        admin = User(
            username='admin',
            email='admin@tvet.com',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            first_name='System',
            last_name='Administrator',
            phone='+254700000000',
            address='Nairobi, Kenya',
            created_at=datetime.utcnow()
        )
        
        # Create lecturer user
        lecturer = User(
            username='lecturer',
            email='lecturer@tvet.com',
            password_hash=generate_password_hash('lecturer123'),
            role='lecturer',
            first_name='John',
            last_name='Doe',
            phone='+254700000001',
            address='Nairobi, Kenya',
            department='ICT Department',
            specialization='Programming',
            created_at=datetime.utcnow()
        )
        
        # Create student user
        student = User(
            username='student',
            email='student@tvet.com',
            password_hash=generate_password_hash('student123'),
            role='student',
            first_name='Jane',
            last_name='Smith',
            phone='+254700000002',
            address='Nairobi, Kenya',
            registration_number='STU2024001',
            course_id=course1.id,
            created_at=datetime.utcnow()
        )
        
        # Create staff user
        staff = User(
            username='staff',
            email='staff@tvet.com',
            password_hash=generate_password_hash('staff123'),
            role='staff',
            first_name='Mary',
            last_name='Johnson',
            phone='+254700000003',
            address='Nairobi, Kenya',
            staff_id='STAFF001',
            position='Registrar',
            department='Administration',
            created_at=datetime.utcnow()
        )
        
        db.session.add(admin)
        db.session.add(lecturer)
        db.session.add(student)
        db.session.add(staff)
        db.session.commit()
        
        # Create sample class rooms (without problematic datetime fields)
        class1 = ClassRoom(
            name='Computer Lab 1',
            description='Main computer laboratory with 30 workstations',
            course_id=course1.id,
            lecturer_id=lecturer.id,
            start_date=datetime(2024, 1, 15).date(),
            end_date=datetime(2024, 12, 15).date(),
            day='monday',
            start_time=datetime(2024, 1, 15, 8, 0),
            end_time=datetime(2024, 1, 15, 12, 0),
            capacity=30
        )
        
        class2 = ClassRoom(
            name='Electrical Lab',
            description='Electrical engineering laboratory',
            course_id=course2.id,
            lecturer_id=lecturer.id,
            start_date=datetime(2024, 1, 15).date(),
            end_date=datetime(2024, 12, 15).date(),
            day='tuesday',
            start_time=datetime(2024, 1, 15, 14, 0),
            end_time=datetime(2024, 1, 15, 18, 0),
            capacity=25
        )
        
        db.session.add(class1)
        db.session.add(class2)
        db.session.commit()
        
        print("Database initialization completed successfully!")
        print("\nSample users created:")
        print("Admin - Username: admin, Password: admin123")
        print("Lecturer - Username: lecturer, Password: lecturer123")
        print("Student - Username: student, Password: student123")
        print("Staff - Username: staff, Password: staff123")

if __name__ == '__main__':
    init_database() 