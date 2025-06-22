#!/usr/bin/env python3
"""
Script to add units for remaining courses that don't have units yet.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Course, Unit

def add_remaining_units():
    """Add units for remaining courses"""
    app = create_app()
    
    with app.app_context():
        # Define units for remaining courses
        remaining_units = {
            # Computer Packages (CP101) - Most important for Kenyan context
            'CP101': [
                {'code': 'CP001', 'name': 'Computer Applications I', 'description': 'Introduction to computer applications and basic software', 'credits': 3},
                {'code': 'CP002', 'name': 'Computer Applications II', 'description': 'Advanced computer applications and productivity tools', 'credits': 3},
                {'code': 'CP003', 'name': 'Microsoft Word Processing', 'description': 'Word processing using Microsoft Word', 'credits': 2},
                {'code': 'CP004', 'name': 'Microsoft Spreadsheets', 'description': 'Spreadsheet applications using Microsoft Excel', 'credits': 2},
                {'code': 'CP005', 'name': 'Microsoft Database', 'description': 'Database management using Microsoft Access', 'credits': 2},
                {'code': 'CP006', 'name': 'Microsoft PowerPoint', 'description': 'Presentation software using Microsoft PowerPoint', 'credits': 2},
                {'code': 'CP007', 'name': 'Internet and Email', 'description': 'Internet browsing and email communication', 'credits': 2},
                {'code': 'CP008', 'name': 'Computer Hardware Basics', 'description': 'Basic computer hardware and troubleshooting', 'credits': 2},
                {'code': 'CP009', 'name': 'Digital Literacy', 'description': 'Digital skills and online safety', 'credits': 2},
                {'code': 'CP010', 'name': 'Office Automation', 'description': 'Office automation and productivity tools', 'credits': 2}
            ],
            
            # ICT102 - Basic ICT course
            'ICT102': [
                {'code': 'ICT201', 'name': 'Computer Fundamentals', 'description': 'Basic computer concepts and operations', 'credits': 3},
                {'code': 'ICT202', 'name': 'Word Processing', 'description': 'Document creation and formatting', 'credits': 2},
                {'code': 'ICT203', 'name': 'Spreadsheets', 'description': 'Data analysis and calculations', 'credits': 2},
                {'code': 'ICT204', 'name': 'Database Management', 'description': 'Basic database operations', 'credits': 2},
                {'code': 'ICT205', 'name': 'Presentation Software', 'description': 'Creating and delivering presentations', 'credits': 2},
                {'code': 'ICT206', 'name': 'Internet Applications', 'description': 'Web browsing and online tools', 'credits': 2},
                {'code': 'ICT207', 'name': 'Computer Maintenance', 'description': 'Basic computer maintenance and troubleshooting', 'credits': 3},
                {'code': 'ICT208', 'name': 'Computer Networks', 'description': 'Introduction to networking concepts', 'credits': 3}
            ],
            
            # FD101 - Fashion Designer
            'FD101': [
                {'code': 'FD201', 'name': 'Fashion Design Basics', 'description': 'Introduction to fashion design principles', 'credits': 3},
                {'code': 'FD202', 'name': 'Pattern Making I', 'description': 'Basic pattern making techniques', 'credits': 4},
                {'code': 'FD203', 'name': 'Garment Construction I', 'description': 'Basic sewing and assembly', 'credits': 4},
                {'code': 'FD204', 'name': 'Fashion Illustration', 'description': 'Fashion drawing and sketching', 'credits': 3},
                {'code': 'FD205', 'name': 'Textile Science', 'description': 'Fabric properties and selection', 'credits': 3},
                {'code': 'FD206', 'name': 'Fashion History', 'description': 'History of fashion and trends', 'credits': 2},
                {'code': 'FD207', 'name': 'Fashion Marketing', 'description': 'Basic fashion business concepts', 'credits': 3},
                {'code': 'FD208', 'name': 'Fashion Merchandising', 'description': 'Fashion retail and merchandising', 'credits': 3}
            ],
            
            # FD102 - Basic Fashion Designer
            'FD102': [
                {'code': 'FD301', 'name': 'Basic Fashion Design', 'description': 'Fundamental fashion design concepts', 'credits': 3},
                {'code': 'FD302', 'name': 'Basic Pattern Making', 'description': 'Simple pattern making techniques', 'credits': 3},
                {'code': 'FD303', 'name': 'Basic Sewing', 'description': 'Fundamental sewing techniques', 'credits': 3},
                {'code': 'FD304', 'name': 'Fabric Knowledge', 'description': 'Understanding different fabrics', 'credits': 2},
                {'code': 'FD305', 'name': 'Fashion Drawing', 'description': 'Basic fashion sketching', 'credits': 2},
                {'code': 'FD306', 'name': 'Garment Fitting', 'description': 'Basic fitting and alterations', 'credits': 2}
            ],
            
            # TM101 - Tailoring or Dress Making
            'TM101': [
                {'code': 'TM001', 'name': 'Basic Tailoring', 'description': 'Fundamental tailoring techniques', 'credits': 3},
                {'code': 'TM002', 'name': 'Pattern Drafting', 'description': 'Basic pattern drafting', 'credits': 3},
                {'code': 'TM003', 'name': 'Sewing Techniques', 'description': 'Essential sewing methods', 'credits': 3},
                {'code': 'TM004', 'name': 'Fabric Selection', 'description': 'Choosing appropriate fabrics', 'credits': 2},
                {'code': 'TM005', 'name': 'Garment Construction', 'description': 'Basic garment assembly', 'credits': 3},
                {'code': 'TM006', 'name': 'Fitting and Alterations', 'description': 'Basic fitting techniques', 'credits': 2}
            ],
            
            # HBT101 - Hairdressing & Beauty Therapy
            'HBT101': [
                {'code': 'HBT001', 'name': 'Hair Care Fundamentals', 'description': 'Basic hair care and treatment', 'credits': 3},
                {'code': 'HBT002', 'name': 'Hair Styling', 'description': 'Hair styling techniques', 'credits': 3},
                {'code': 'HBT003', 'name': 'Hair Coloring', 'description': 'Hair coloring and treatment', 'credits': 3},
                {'code': 'HBT004', 'name': 'Beauty Therapy', 'description': 'Basic beauty treatments', 'credits': 3},
                {'code': 'HBT005', 'name': 'Skin Care', 'description': 'Skin care and treatments', 'credits': 3},
                {'code': 'HBT006', 'name': 'Nail Care', 'description': 'Manicure and pedicure', 'credits': 2},
                {'code': 'HBT007', 'name': 'Makeup Application', 'description': 'Professional makeup techniques', 'credits': 3},
                {'code': 'HBT008', 'name': 'Salon Management', 'description': 'Salon operations and management', 'credits': 3}
            ],
            
            # HBT102 - Hairdressing & Beauty Therapy (Basic)
            'HBT102': [
                {'code': 'HBT101', 'name': 'Basic Hair Care', 'description': 'Fundamental hair care', 'credits': 3},
                {'code': 'HBT102', 'name': 'Basic Hair Styling', 'description': 'Simple hair styling', 'credits': 3},
                {'code': 'HBT103', 'name': 'Basic Beauty Care', 'description': 'Fundamental beauty treatments', 'credits': 3},
                {'code': 'HBT104', 'name': 'Basic Skin Care', 'description': 'Simple skin care techniques', 'credits': 2},
                {'code': 'HBT105', 'name': 'Basic Nail Care', 'description': 'Simple nail care', 'credits': 2}
            ],
            
            # HBT103 - Hairdressing & Beauty Therapy (Artisan)
            'HBT103': [
                {'code': 'HBT201', 'name': 'Hair Washing and Treatment', 'description': 'Basic hair washing and treatment', 'credits': 2},
                {'code': 'HBT202', 'name': 'Simple Hair Styling', 'description': 'Basic hair styling techniques', 'credits': 2},
                {'code': 'HBT203', 'name': 'Basic Beauty Care', 'description': 'Simple beauty treatments', 'credits': 2},
                {'code': 'HBT204', 'name': 'Salon Hygiene', 'description': 'Salon cleanliness and hygiene', 'credits': 1}
            ],
            
            # WF102 - Welding (Artisan)
            'WF102': [
                {'code': 'WF201', 'name': 'Basic Welding Safety', 'description': 'Welding safety procedures', 'credits': 2},
                {'code': 'WF202', 'name': 'Arc Welding Basics', 'description': 'Basic arc welding techniques', 'credits': 3},
                {'code': 'WF203', 'name': 'Gas Welding Basics', 'description': 'Basic gas welding and cutting', 'credits': 3},
                {'code': 'WF204', 'name': 'Metal Cutting', 'description': 'Basic metal cutting techniques', 'credits': 2},
                {'code': 'WF205', 'name': 'Basic Fabrication', 'description': 'Simple metal fabrication', 'credits': 3}
            ],
            
            # AT102 - Automotive Technician (Artisan)
            'AT102': [
                {'code': 'AT201', 'name': 'Basic Engine Maintenance', 'description': 'Simple engine maintenance', 'credits': 3},
                {'code': 'AT202', 'name': 'Basic Electrical Systems', 'description': 'Simple electrical repairs', 'credits': 3},
                {'code': 'AT203', 'name': 'Basic Brake Systems', 'description': 'Simple brake maintenance', 'credits': 2},
                {'code': 'AT204', 'name': 'Basic Suspension', 'description': 'Simple suspension work', 'credits': 2},
                {'code': 'AT205', 'name': 'Basic Diagnostics', 'description': 'Simple vehicle diagnostics', 'credits': 3}
            ],
            
            # DC101 - Driving Classes
            'DC101': [
                {'code': 'DC001', 'name': 'Traffic Rules and Regulations', 'description': 'Kenyan traffic laws and rules', 'credits': 2},
                {'code': 'DC002', 'name': 'Vehicle Controls', 'description': 'Understanding vehicle controls', 'credits': 2},
                {'code': 'DC003', 'name': 'Basic Driving Skills', 'description': 'Fundamental driving techniques', 'credits': 3},
                {'code': 'DC004', 'name': 'Road Safety', 'description': 'Road safety and defensive driving', 'credits': 2},
                {'code': 'DC005', 'name': 'Vehicle Maintenance', 'description': 'Basic vehicle maintenance', 'credits': 2}
            ],
            
            # PL102 - Plumbing (Artisan)
            'PL102': [
                {'code': 'PL201', 'name': 'Basic Plumbing Tools', 'description': 'Plumbing tools and equipment', 'credits': 2},
                {'code': 'PL202', 'name': 'Basic Pipe Fitting', 'description': 'Simple pipe installation', 'credits': 3},
                {'code': 'PL203', 'name': 'Basic Fixture Installation', 'description': 'Simple fixture installation', 'credits': 2},
                {'code': 'PL204', 'name': 'Basic Maintenance', 'description': 'Simple plumbing maintenance', 'credits': 2},
                {'code': 'PL205', 'name': 'Plumbing Safety', 'description': 'Safety in plumbing work', 'credits': 1}
            ],
            
            # BA101 - Building Artisan (Masonry)
            'BA101': [
                {'code': 'BA001', 'name': 'Basic Masonry', 'description': 'Fundamental masonry techniques', 'credits': 3},
                {'code': 'BA002', 'name': 'Brick Laying', 'description': 'Brick laying techniques', 'credits': 3},
                {'code': 'BA003', 'name': 'Block Laying', 'description': 'Block laying techniques', 'credits': 3},
                {'code': 'BA004', 'name': 'Concrete Work', 'description': 'Basic concrete mixing and placement', 'credits': 3},
                {'code': 'BA005', 'name': 'Building Materials', 'description': 'Understanding building materials', 'credits': 2},
                {'code': 'BA006', 'name': 'Safety in Construction', 'description': 'Construction site safety', 'credits': 2}
            ],
            
            # FP101 - Food Production (Culinary Arts)
            'FP101': [
                {'code': 'FP201', 'name': 'Food Safety and Hygiene', 'description': 'Kitchen safety and hygiene', 'credits': 3},
                {'code': 'FP202', 'name': 'Basic Food Preparation', 'description': 'Fundamental cooking techniques', 'credits': 4},
                {'code': 'FP203', 'name': 'Culinary Arts I', 'description': 'Basic culinary techniques', 'credits': 4},
                {'code': 'FP204', 'name': 'Bakery Basics', 'description': 'Basic baking techniques', 'credits': 3},
                {'code': 'FP205', 'name': 'Menu Planning', 'description': 'Basic menu planning', 'credits': 2},
                {'code': 'FP206', 'name': 'Kitchen Management', 'description': 'Basic kitchen operations', 'credits': 3},
                {'code': 'FP207', 'name': 'Nutrition Basics', 'description': 'Basic nutrition principles', 'credits': 2}
            ],
            
            # FP102 - Food Production (Short Course)
            'FP102': [
                {'code': 'FP301', 'name': 'Food Safety', 'description': 'Basic food safety', 'credits': 2},
                {'code': 'FP302', 'name': 'Basic Cooking', 'description': 'Simple cooking techniques', 'credits': 3},
                {'code': 'FP303', 'name': 'Kitchen Hygiene', 'description': 'Kitchen cleanliness', 'credits': 2},
                {'code': 'FP304', 'name': 'Food Storage', 'description': 'Proper food storage', 'credits': 2}
            ],
            
            # FP103 - Food Production (Basic)
            'FP103': [
                {'code': 'FP401', 'name': 'Kitchen Safety', 'description': 'Basic kitchen safety', 'credits': 2},
                {'code': 'FP402', 'name': 'Simple Food Preparation', 'description': 'Basic food preparation', 'credits': 3},
                {'code': 'FP403', 'name': 'Food Hygiene', 'description': 'Basic food hygiene', 'credits': 2}
            ],
            
            # SCM102 - Supply Chain Management (Basic)
            'SCM102': [
                {'code': 'SCM201', 'name': 'Supply Chain Basics', 'description': 'Introduction to supply chain', 'credits': 3},
                {'code': 'SCM202', 'name': 'Basic Procurement', 'description': 'Simple procurement processes', 'credits': 3},
                {'code': 'SCM203', 'name': 'Basic Inventory', 'description': 'Simple inventory management', 'credits': 3},
                {'code': 'SCM204', 'name': 'Basic Warehousing', 'description': 'Simple warehouse operations', 'credits': 3},
                {'code': 'SCM205', 'name': 'Basic Transportation', 'description': 'Simple transportation concepts', 'credits': 3}
            ],
            
            # OA102 - Office Administrator
            'OA102': [
                {'code': 'OA201', 'name': 'Office Management Basics', 'description': 'Basic office management', 'credits': 3},
                {'code': 'OA202', 'name': 'Business Communication', 'description': 'Effective communication', 'credits': 3},
                {'code': 'OA203', 'name': 'Records Management', 'description': 'Basic records management', 'credits': 3},
                {'code': 'OA204', 'name': 'Customer Service', 'description': 'Customer service skills', 'credits': 2},
                {'code': 'OA205', 'name': 'Office Technology', 'description': 'Office equipment and software', 'credits': 3}
            ],
            
            # OA103 - Office Assistant
            'OA103': [
                {'code': 'OA301', 'name': 'Basic Office Skills', 'description': 'Fundamental office skills', 'credits': 3},
                {'code': 'OA302', 'name': 'Communication Skills', 'description': 'Basic communication', 'credits': 2},
                {'code': 'OA303', 'name': 'File Management', 'description': 'Basic file organization', 'credits': 2},
                {'code': 'OA304', 'name': 'Office Equipment', 'description': 'Basic office equipment use', 'credits': 2}
            ],
            
            # SW102 - Social Work (Basic)
            'SW102': [
                {'code': 'SW201', 'name': 'Social Work Basics', 'description': 'Introduction to social work', 'credits': 3},
                {'code': 'SW202', 'name': 'Community Development Basics', 'description': 'Basic community work', 'credits': 3},
                {'code': 'SW203', 'name': 'Communication Skills', 'description': 'Effective communication', 'credits': 2},
                {'code': 'SW204', 'name': 'Basic Counseling', 'description': 'Simple counseling techniques', 'credits': 3},
                {'code': 'SW205', 'name': 'Social Issues', 'description': 'Understanding social problems', 'credits': 3}
            ],
            
            # FT102 - Food Technology (Basic)
            'FT102': [
                {'code': 'FT201', 'name': 'Food Science Basics', 'description': 'Basic food science', 'credits': 3},
                {'code': 'FT202', 'name': 'Food Processing Basics', 'description': 'Basic food processing', 'credits': 3},
                {'code': 'FT203', 'name': 'Food Safety Basics', 'description': 'Basic food safety', 'credits': 3},
                {'code': 'FT204', 'name': 'Food Analysis Basics', 'description': 'Basic food testing', 'credits': 3},
                {'code': 'FT205', 'name': 'Food Packaging Basics', 'description': 'Basic food packaging', 'credits': 2}
            ],
            
            # SLT102 - Science Laboratory Technology (Basic)
            'SLT102': [
                {'code': 'SLT201', 'name': 'Laboratory Safety Basics', 'description': 'Basic lab safety', 'credits': 2},
                {'code': 'SLT202', 'name': 'Basic Chemistry', 'description': 'Simple chemical analysis', 'credits': 3},
                {'code': 'SLT203', 'name': 'Basic Microbiology', 'description': 'Simple microbiological work', 'credits': 3},
                {'code': 'SLT204', 'name': 'Laboratory Equipment', 'description': 'Basic lab equipment use', 'credits': 3},
                {'code': 'SLT205', 'name': 'Quality Control Basics', 'description': 'Basic quality control', 'credits': 2}
            ],
            
            # ICT001 - Information Technology (if different from ICT101)
            'ICT001': [
                {'code': 'IT001', 'name': 'Computer Fundamentals', 'description': 'Basic computer concepts', 'credits': 3},
                {'code': 'IT002', 'name': 'Programming Basics', 'description': 'Introduction to programming', 'credits': 4},
                {'code': 'IT003', 'name': 'Web Development', 'description': 'Basic web development', 'credits': 4},
                {'code': 'IT004', 'name': 'Database Systems', 'description': 'Database design and management', 'credits': 4},
                {'code': 'IT005', 'name': 'Network Administration', 'description': 'Computer networking', 'credits': 4},
                {'code': 'IT006', 'name': 'System Administration', 'description': 'Computer system management', 'credits': 4},
                {'code': 'IT007', 'name': 'Cybersecurity', 'description': 'Information security', 'credits': 3},
                {'code': 'IT008', 'name': 'IT Project Management', 'description': 'IT project planning', 'credits': 3}
            ]
        }
        
        total_units_created = 0
        
        for course_code, units_data in remaining_units.items():
            # Find the course
            course = Course.query.filter_by(code=course_code).first()
            if not course:
                print(f"Course {course_code} not found")
                continue
            
            # Check if units already exist
            existing_units = Unit.query.filter_by(course_id=course.id).count()
            if existing_units > 0:
                print(f"Course {course_code} already has {existing_units} units")
                continue
            
            # Create units for this course
            units_created = 0
            for unit_data in units_data:
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
                    print(f"Error creating unit {unit_data['code']}: {e}")
                    db.session.rollback()
                    continue
            
            # Commit units for this course
            try:
                db.session.commit()
                print(f"Created {units_created} units for {course_code}")
                total_units_created += units_created
            except Exception as e:
                print(f"Error committing units for {course_code}: {e}")
                db.session.rollback()
        
        print(f"\nTotal additional units created: {total_units_created}")
        print("Remaining units import completed!")

if __name__ == '__main__':
    add_remaining_units() 