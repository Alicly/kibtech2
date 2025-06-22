from app.models import Course

def create_courses(lecturer_id):
    courses = [
        # Agriculture and Environmental Studies
        Course(
            code='AEXT101',
            name='Agriculture Extension',
            description='Training in agricultural extension services and rural development',
            duration='2 years',
            level='Certificate',
            category='Agriculture',
            capacity=30,
            fee=500.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='SARD101',
            name='Sustainable Agriculture for Rural Development',
            description='Training in sustainable agricultural practices for rural development',
            duration='1 year',
            level='Certificate',
            category='Agriculture',
            capacity=30,
            fee=400.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='AEXT102',
            name='Agricultural Extension',
            description='Short course in agricultural extension services',
            duration='6 months',
            level='Certificate',
            category='Agriculture',
            capacity=20,
            fee=300.00,
            lecturer_id=lecturer_id
        ),

        # Electrical and Electronics Engineering
        Course(
            code='ELE101',
            name='Electrical Engineering (Power option)',
            description='Training in electrical engineering with focus on power systems',
            duration='2 years',
            level='Certificate',
            category='Electrical',
            capacity=30,
            fee=600.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='ELE102',
            name='Electrical Operations',
            description='Training in electrical operations and maintenance',
            duration='1 year',
            level='Certificate',
            category='Electrical',
            capacity=25,
            fee=450.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='ELE103',
            name='Electrical Artisan',
            description='Basic electrical installation and maintenance',
            duration='6 months',
            level='Certificate',
            category='Electrical',
            capacity=20,
            fee=300.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='ELE104',
            name='Electrical Installation',
            description='Basic electrical installation course',
            duration='6 months',
            level='Certificate',
            category='Electrical',
            capacity=20,
            fee=300.00,
            lecturer_id=lecturer_id
        ),

        # Fashion Design and Cosmetology
        Course(
            code='FDM101',
            name='Fashion Design Manager',
            description='Advanced training in fashion design management',
            duration='2 years',
            level='Certificate',
            category='Fashion',
            capacity=25,
            fee=550.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='FD101',
            name='Fashion Designer',
            description='Training in fashion design and garment making',
            duration='1 year',
            level='Certificate',
            category='Fashion',
            capacity=25,
            fee=450.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='FD102',
            name='Fashion Designer',
            description='Basic fashion design course',
            duration='6 months',
            level='Certificate',
            category='Fashion',
            capacity=20,
            fee=300.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='TM101',
            name='Tailoring or Dress Making',
            description='Basic tailoring and dress making course',
            duration='6 months',
            level='Certificate',
            category='Fashion',
            capacity=20,
            fee=300.00,
            lecturer_id=lecturer_id
        ),

        # Mechanical and Automotive Engineering
        Course(
            code='WF101',
            name='Welding & Fabrication',
            description='Training in welding and metal fabrication',
            duration='1 year',
            level='Certificate',
            category='Mechanical',
            capacity=25,
            fee=500.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='AT101',
            name='Automotive Technician',
            description='Training in automotive repair and maintenance',
            duration='1 year',
            level='Certificate',
            category='Mechanical',
            capacity=25,
            fee=500.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='AT102',
            name='Automotive Technician',
            description='Basic automotive repair and maintenance',
            duration='6 months',
            level='Certificate',
            category='Mechanical',
            capacity=20,
            fee=350.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='WF102',
            name='Welding (manual metal arc welding)',
            description='Basic welding course',
            duration='6 months',
            level='Certificate',
            category='Mechanical',
            capacity=20,
            fee=350.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='DC101',
            name='Driving Classes',
            description='Professional driving course',
            duration='1 month',
            level='Certificate',
            category='Mechanical',
            capacity=15,
            fee=200.00,
            lecturer_id=lecturer_id
        ),

        # Building and Civil Engineering
        Course(
            code='BT101',
            name='Building Technician',
            description='Training in building construction and management',
            duration='2 years',
            level='Certificate',
            category='Civil',
            capacity=30,
            fee=600.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='CE101',
            name='Civil Engineering',
            description='Basic civil engineering course',
            duration='1 year',
            level='Certificate',
            category='Civil',
            capacity=25,
            fee=500.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='PL101',
            name='Plumbing',
            description='Training in plumbing installation and maintenance',
            duration='1 year',
            level='Certificate',
            category='Civil',
            capacity=25,
            fee=450.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='PL102',
            name='Plumbing',
            description='Basic plumbing course',
            duration='5 months',
            level='Certificate',
            category='Civil',
            capacity=20,
            fee=300.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='BA101',
            name='Building Artisan (masonry)',
            description='Basic masonry and construction course',
            duration='6 months',
            level='Certificate',
            category='Civil',
            capacity=20,
            fee=300.00,
            lecturer_id=lecturer_id
        ),

        # Hospitality and Institutional Management
        Course(
            code='FBP101',
            name='Food and Beverage Production (Culinary arts)',
            description='Professional culinary arts training',
            duration='2 years',
            level='Certificate',
            category='Hospitality',
            capacity=25,
            fee=550.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='FP101',
            name='Food Production (Culinary arts)',
            description='Basic culinary arts training',
            duration='1 year',
            level='Certificate',
            category='Hospitality',
            capacity=25,
            fee=450.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='FP102',
            name='Food Production (Culinary arts)',
            description='Short course in food production',
            duration='6 months',
            level='Certificate',
            category='Hospitality',
            capacity=20,
            fee=300.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='FP103',
            name='Food Production (Culinary arts)',
            description='Basic food preparation course',
            duration='6 months',
            level='Certificate',
            category='Hospitality',
            capacity=20,
            fee=300.00,
            lecturer_id=lecturer_id
        ),

        # Business Studies
        Course(
            code='SCM101',
            name='Supply Chain Management',
            description='Professional supply chain management training',
            duration='2 years',
            level='Certificate',
            category='Business',
            capacity=30,
            fee=600.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='SCM102',
            name='Supply Chain Management',
            description='Basic supply chain management course',
            duration='1 year',
            level='Certificate',
            category='Business',
            capacity=25,
            fee=450.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='ACC101',
            name='Accountancy',
            description='Professional accounting training',
            duration='2 years',
            level='Certificate',
            category='Business',
            capacity=30,
            fee=600.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='BM101',
            name='Business Management',
            description='Basic business management course',
            duration='1 year',
            level='Certificate',
            category='Business',
            capacity=25,
            fee=450.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='OA101',
            name='Office Administration',
            description='Professional office administration training',
            duration='2 years',
            level='Certificate',
            category='Business',
            capacity=30,
            fee=600.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='OA102',
            name='Office Administrator',
            description='Basic office administration course',
            duration='1 year',
            level='Certificate',
            category='Business',
            capacity=25,
            fee=450.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='OA103',
            name='Office Assistant',
            description='Basic office skills course',
            duration='6 months',
            level='Certificate',
            category='Business',
            capacity=20,
            fee=300.00,
            lecturer_id=lecturer_id
        ),

        # Computing and Informatics
        Course(
            code='ICT101',
            name='ICT Technician',
            description='Professional ICT training',
            duration='2 years',
            level='Certificate',
            category='ICT',
            capacity=30,
            fee=600.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='ICT102',
            name='ICT Technician',
            description='Basic ICT course',
            duration='1 year',
            level='Certificate',
            category='ICT',
            capacity=25,
            fee=450.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='LIS101',
            name='Library and Information Science',
            description='Professional library science training',
            duration='2 years',
            level='Certificate',
            category='ICT',
            capacity=25,
            fee=550.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='LIS102',
            name='Library and Information Science',
            description='Basic library science course',
            duration='1 year',
            level='Certificate',
            category='ICT',
            capacity=25,
            fee=450.00,
            lecturer_id=lecturer_id
        ),

        # Liberal Studies
        Course(
            code='SW101',
            name='Social Work and Community Development',
            description='Professional social work training',
            duration='2 years',
            level='Certificate',
            category='Liberal',
            capacity=30,
            fee=550.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='SW102',
            name='Social Work and Community Development',
            description='Basic social work course',
            duration='1 year',
            level='Certificate',
            category='Liberal',
            capacity=25,
            fee=450.00,
            lecturer_id=lecturer_id
        ),

        # Applied Sciences
        Course(
            code='FT101',
            name='Food Technology',
            description='Professional food technology training',
            duration='2 years',
            level='Certificate',
            category='Science',
            capacity=25,
            fee=550.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='FT102',
            name='Food Technology',
            description='Basic food technology course',
            duration='1 year',
            level='Certificate',
            category='Science',
            capacity=25,
            fee=450.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='SLT101',
            name='Science Laboratory Technology',
            description='Professional laboratory technology training',
            duration='2 years',
            level='Certificate',
            category='Science',
            capacity=25,
            fee=550.00,
            lecturer_id=lecturer_id
        ),
        Course(
            code='SLT102',
            name='Science Laboratory Technology',
            description='Basic laboratory technology course',
            duration='1 year',
            level='Certificate',
            category='Science',
            capacity=25,
            fee=450.00,
            lecturer_id=lecturer_id
        )
    ]
    return courses 