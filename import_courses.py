from app import create_app, db
from app.models import Course, User
from datetime import datetime
from werkzeug.security import generate_password_hash

def import_courses():
    app = create_app()
    with app.app_context():
        # Get or create the lecturer user
        lecturer = User.query.filter_by(role='lecturer').first()
        if not lecturer:
            print("Creating lecturer user...")
            lecturer = User(
                username='lecturer',
                email='lecturer@kitelakapeltti.edu',
                password_hash=generate_password_hash('lecturer123'),
                first_name='John',
                last_name='Doe',
                role='lecturer',
                lecturer_id='L001'
            )
            db.session.add(lecturer)
            db.session.commit()
            print("Lecturer user created successfully!")

        # Course data
        courses = [
            # Agriculture & Environmental Studies
            {
                'code': 'AEXT101',
                'name': 'Agriculture Extension',
                'description': 'Training in agricultural extension services and rural development',
                'duration': '2 years',
                'level': 'Certificate II',
                'category': 'Agriculture',
                'entry_requirements': 'KCSE Mean Grade C- or KNEC Craft',
                'exam_body': 'TVET-CDACC',
                'capacity': 30,
                'fee': 500.00
            },
            {
                'code': 'SARD101',
                'name': 'Sustainable Agriculture for Rural Development',
                'description': 'Training in sustainable agricultural practices for rural development',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Agriculture',
                'entry_requirements': 'KCSE Mean Grade D (Plain)',
                'exam_body': 'TVET-CDACC',
                'capacity': 30,
                'fee': 400.00
            },
            {
                'code': 'AEXT102',
                'name': 'Agricultural Extension (Artisan)',
                'description': 'Short course in agricultural extension services',
                'duration': '6 months',
                'level': 'Level 3',
                'category': 'Agriculture',
                'entry_requirements': 'KCSE Certificate',
                'exam_body': 'TVET-CDACC',
                'capacity': 20,
                'fee': 300.00
            },
            # Electrical & Electronics Engineering
            {
                'code': 'ELE101',
                'name': 'Electrical Engineering (Power Option)',
                'description': 'Training in electrical engineering with focus on power systems',
                'duration': '2 years',
                'level': 'Certificate II',
                'category': 'Electrical',
                'entry_requirements': 'KCSE Mean Grade C- or KNEC Craft',
                'exam_body': 'TVET-CDACC',
                'capacity': 30,
                'fee': 600.00
            },
            {
                'code': 'ELE102',
                'name': 'Electrical Operations',
                'description': 'Training in electrical operations and maintenance',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Electrical',
                'entry_requirements': 'KCSE Mean Grade D (Plain) or Artisan (Pass in all units)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 450.00
            },
            {
                'code': 'ELE103',
                'name': 'Electrical Installation (Artisan)',
                'description': 'Basic electrical installation and maintenance',
                'duration': '6 months',
                'level': 'Level 3',
                'category': 'Electrical',
                'entry_requirements': 'KCSE Certificate',
                'exam_body': 'TVET-CDACC',
                'capacity': 20,
                'fee': 300.00
            },
            {
                'code': 'ELE104',
                'name': 'Electrical Installation (Basic)',
                'description': 'Basic electrical installation course',
                'duration': '6 months',
                'level': 'Artisan',
                'category': 'Electrical',
                'entry_requirements': 'KCPE Certificate',
                'exam_body': 'TVET-CDACC',
                'capacity': 20,
                'fee': 300.00
            },
            # Fashion Design & Cosmetology
            {
                'code': 'FDM101',
                'name': 'Fashion Design Manager',
                'description': 'Advanced training in fashion design management',
                'duration': '2 years',
                'level': 'Certificate II',
                'category': 'Fashion',
                'entry_requirements': 'KCSE Mean Grade C- or KNEC Craft',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 550.00
            },
            {
                'code': 'FD101',
                'name': 'Fashion Designer',
                'description': 'Training in fashion design and garment making',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Fashion',
                'entry_requirements': 'KCSE Mean Grade D (Plain)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 450.00
            },
            {
                'code': 'FD102',
                'name': 'Fashion Designer (Artisan)',
                'description': 'Basic fashion design course',
                'duration': '6 months',
                'level': 'Level 3',
                'category': 'Fashion',
                'entry_requirements': 'KCSE Certificate',
                'exam_body': 'TVET-CDACC',
                'capacity': 20,
                'fee': 300.00
            },
            {
                'code': 'TM101',
                'name': 'Tailoring / Dressmaking (Artisan)',
                'description': 'Basic tailoring and dress making course',
                'duration': '6 months',
                'level': 'Artisan',
                'category': 'Fashion',
                'entry_requirements': 'KCPE Certificate',
                'exam_body': 'TVET-CDACC',
                'capacity': 20,
                'fee': 300.00
            },
            {
                'code': 'HBT101',
                'name': 'Hairdressing & Beauty Therapy',
                'description': 'Professional hairdressing and beauty therapy training',
                'duration': '2 years',
                'level': 'Certificate II',
                'category': 'Fashion',
                'entry_requirements': 'KCSE Mean Grade C- or KNEC Craft',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 550.00
            },
            {
                'code': 'HBT102',
                'name': 'Hairdressing & Beauty Therapy',
                'description': 'Basic hairdressing and beauty therapy training',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Fashion',
                'entry_requirements': 'KCSE Mean Grade D (Plain)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 450.00
            },
            {
                'code': 'HBT103',
                'name': 'Hairdressing & Beauty Therapy (Artisan)',
                'description': 'Short course in hairdressing and beauty therapy',
                'duration': '6 months',
                'level': 'Artisan',
                'category': 'Fashion',
                'entry_requirements': 'KCSE Certificate / KCPE Cert.',
                'exam_body': 'TVET-CDACC',
                'capacity': 20,
                'fee': 300.00
            },
            # Mechanical & Automotive Engineering
            {
                'code': 'WF101',
                'name': 'Welding & Fabrication',
                'description': 'Training in welding and metal fabrication',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Mechanical',
                'entry_requirements': 'KCSE Mean Grade D (Plain) or Artisan (Pass in all units)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 500.00
            },
            {
                'code': 'WF102',
                'name': 'Welding & Fabrication (Artisan)',
                'description': 'Basic welding course',
                'duration': '6 months',
                'level': 'Artisan',
                'category': 'Mechanical',
                'entry_requirements': 'KCSE Certificate / KCPE Certificate',
                'exam_body': 'TVET-CDACC',
                'capacity': 20,
                'fee': 350.00
            },
            {
                'code': 'AT101',
                'name': 'Automotive Technician',
                'description': 'Training in automotive repair and maintenance',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Mechanical',
                'entry_requirements': 'KCSE Mean Grade D (Plain) or Artisan (Pass in all units)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 500.00
            },
            {
                'code': 'AT102',
                'name': 'Automotive Technician (Artisan)',
                'description': 'Basic automotive repair and maintenance',
                'duration': '6 months',
                'level': 'Artisan',
                'category': 'Mechanical',
                'entry_requirements': 'KCSE Mean Grade D (Plain)',
                'exam_body': 'TVET-CDACC',
                'capacity': 20,
                'fee': 350.00
            },
            {
                'code': 'DC101',
                'name': 'Driving Classes',
                'description': 'Professional driving course',
                'duration': '1 month',
                'level': 'N/A',
                'category': 'Mechanical',
                'entry_requirements': '18 Years & Above',
                'exam_body': 'NTSA',
                'capacity': 15,
                'fee': 200.00
            },
            # Building & Civil Engineering
            {
                'code': 'BT101',
                'name': 'Building Technician',
                'description': 'Training in building construction and management',
                'duration': '2 years',
                'level': 'Certificate II',
                'category': 'Civil',
                'entry_requirements': 'KCSE Mean Grade C- or KNEC Craft',
                'exam_body': 'TVET-CDACC',
                'capacity': 30,
                'fee': 600.00
            },
            {
                'code': 'CE101',
                'name': 'Civil Engineering Technician',
                'description': 'Basic civil engineering course',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Civil',
                'entry_requirements': 'KCSE Mean Grade D (Plain)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 500.00
            },
            {
                'code': 'PL101',
                'name': 'Plumbing',
                'description': 'Training in plumbing installation and maintenance',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Civil',
                'entry_requirements': 'KCSE Mean Grade D (Plain) or Artisan (Pass in all units)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 450.00
            },
            {
                'code': 'PL102',
                'name': 'Plumbing (Artisan)',
                'description': 'Basic plumbing course',
                'duration': '5 months',
                'level': 'Artisan',
                'category': 'Civil',
                'entry_requirements': 'KCSE Certificate',
                'exam_body': 'TVET-CDACC',
                'capacity': 20,
                'fee': 300.00
            },
            {
                'code': 'BA101',
                'name': 'Building Artisan (Masonry)',
                'description': 'Basic masonry and construction course',
                'duration': '6 months',
                'level': 'Artisan',
                'category': 'Civil',
                'entry_requirements': 'KCSE Certificate',
                'exam_body': 'TVET-CDACC',
                'capacity': 20,
                'fee': 300.00
            },
            # Hospitality & Institutional Management
            {
                'code': 'FBP101',
                'name': 'Food & Beverage Production (Culinary Arts)',
                'description': 'Professional culinary arts training',
                'duration': '2 years',
                'level': 'Certificate II',
                'category': 'Hospitality',
                'entry_requirements': 'KCSE Mean Grade C- or KNEC Craft',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 550.00
            },
            {
                'code': 'FP101',
                'name': 'Food Production (Culinary Arts)',
                'description': 'Basic culinary arts training',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Hospitality',
                'entry_requirements': 'KCSE Mean Grade D (Plain)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 450.00
            },
            {
                'code': 'FP102',
                'name': 'Food Production (Culinary Arts)',
                'description': 'Short course in food production',
                'duration': '6 months',
                'level': 'Artisan',
                'category': 'Hospitality',
                'entry_requirements': 'KCSE Certificate / KCPE Cert.',
                'exam_body': 'TVET-CDACC',
                'capacity': 20,
                'fee': 300.00
            },
            # Business Studies
            {
                'code': 'SCM101',
                'name': 'Supply Chain Management',
                'description': 'Professional supply chain management training',
                'duration': '2 years',
                'level': 'Certificate II',
                'category': 'Business',
                'entry_requirements': 'KCSE Mean Grade C- or KNEC Craft',
                'exam_body': 'TVET-CDACC',
                'capacity': 30,
                'fee': 600.00
            },
            {
                'code': 'SCM102',
                'name': 'Supply Chain Management',
                'description': 'Basic supply chain management course',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Business',
                'entry_requirements': 'KCSE Mean Grade D (Plain)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 450.00
            },
            {
                'code': 'ACC101',
                'name': 'Accountancy',
                'description': 'Professional accounting training',
                'duration': '2 years',
                'level': 'Certificate II',
                'category': 'Business',
                'entry_requirements': 'KCSE Mean Grade C- or KNEC Craft',
                'exam_body': 'TVET-CDACC',
                'capacity': 30,
                'fee': 600.00
            },
            {
                'code': 'BM101',
                'name': 'Business Management',
                'description': 'Basic business management course',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Business',
                'entry_requirements': 'KCSE Mean Grade D (Plain)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 450.00
            },
            {
                'code': 'OA101',
                'name': 'Office Administration',
                'description': 'Professional office administration training',
                'duration': '2 years',
                'level': 'Certificate II',
                'category': 'Business',
                'entry_requirements': 'KCSE Mean Grade C- or KNEC Craft',
                'exam_body': 'TVET-CDACC',
                'capacity': 30,
                'fee': 600.00
            },
            {
                'code': 'OA102',
                'name': 'Office Administrator',
                'description': 'Basic office administration course',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Business',
                'entry_requirements': 'KCSE Mean Grade D (Plain)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 450.00
            },
            {
                'code': 'OA103',
                'name': 'Office Assistant',
                'description': 'Basic office skills course',
                'duration': '6 months',
                'level': 'Artisan',
                'category': 'Business',
                'entry_requirements': 'KCPE Certificate',
                'exam_body': 'TVET-CDACC',
                'capacity': 20,
                'fee': 300.00
            },
            # Computing & Informatics
            {
                'code': 'ICT101',
                'name': 'ICT Technician',
                'description': 'Professional ICT training',
                'duration': '2 years',
                'level': 'Certificate II',
                'category': 'ICT',
                'entry_requirements': 'KCSE Mean Grade C- or KNEC Craft',
                'exam_body': 'TVET-CDACC',
                'capacity': 30,
                'fee': 600.00
            },
            {
                'code': 'ICT102',
                'name': 'ICT Technician',
                'description': 'Basic ICT course',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'ICT',
                'entry_requirements': 'KCSE Mean Grade D (Plain)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 450.00
            },
            {
                'code': 'CP101',
                'name': 'Computer Packages',
                'description': 'Short course in computer applications',
                'duration': 'Flexible',
                'level': 'Short Course',
                'category': 'ICT',
                'entry_requirements': 'Open (KTTI Internal)',
                'exam_body': 'KTTI',
                'capacity': 20,
                'fee': 250.00
            },
            # Liberal Studies
            {
                'code': 'SW101',
                'name': 'Social Work & Community Development',
                'description': 'Professional social work training',
                'duration': '2 years',
                'level': 'Certificate II',
                'category': 'Liberal',
                'entry_requirements': 'KCSE Mean Grade C- or KNEC Craft',
                'exam_body': 'TVET-CDACC',
                'capacity': 30,
                'fee': 550.00
            },
            {
                'code': 'SW102',
                'name': 'Social Work & Community Development',
                'description': 'Basic social work course',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Liberal',
                'entry_requirements': 'KCSE Mean Grade D (Plain)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 450.00
            },
            # Applied Sciences
            {
                'code': 'FT101',
                'name': 'Food Technology',
                'description': 'Professional food technology training',
                'duration': '2 years',
                'level': 'Certificate II',
                'category': 'Science',
                'entry_requirements': 'KCSE Mean Grade C- or KNEC Craft',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 550.00
            },
            {
                'code': 'FT102',
                'name': 'Food Technology',
                'description': 'Basic food technology course',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Science',
                'entry_requirements': 'KCSE Mean Grade D (Plain)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 450.00
            },
            {
                'code': 'SLT101',
                'name': 'Science Laboratory Technology',
                'description': 'Professional laboratory technology training',
                'duration': '2 years',
                'level': 'Certificate II',
                'category': 'Science',
                'entry_requirements': 'KCSE Mean Grade C- or KNEC Craft',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 550.00
            },
            {
                'code': 'SLT102',
                'name': 'Science Laboratory Technology',
                'description': 'Basic laboratory technology course',
                'duration': '1 year',
                'level': 'Level 4',
                'category': 'Science',
                'entry_requirements': 'KCSE Mean Grade D (Plain)',
                'exam_body': 'TVET-CDACC',
                'capacity': 25,
                'fee': 450.00
            }
        ]

        # Create courses
        for course_data in courses:
            # Check if course already exists
            existing_course = Course.query.filter_by(code=course_data['code']).first()
            if existing_course:
                print(f"Course {course_data['code']} already exists, skipping...")
                continue

            # Create new course
            course = Course(
                code=course_data['code'],
                name=course_data['name'],
                description=course_data['description'],
                duration=course_data['duration'],
                level=course_data['level'],
                category=course_data['category'],
                capacity=course_data['capacity'],
                fee=course_data['fee'],
                lecturer_id=lecturer.id,
                entry_requirements=course_data['entry_requirements'],
                exam_body=course_data['exam_body']
            )
            db.session.add(course)
            print(f"Added course: {course_data['code']} - {course_data['name']}")

        # Commit all changes
        db.session.commit()
        print("\nAll courses have been imported successfully!")

if __name__ == '__main__':
    import_courses() 