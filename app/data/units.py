from app.models import Unit

def create_units():
    units_data = {
        # Computer Packages (ICT101, ICT102) - Most common units
        'ICT101': [
            {'code': 'ICT001', 'name': 'Computer Applications I', 'description': 'Introduction to computer applications and basic software', 'credits': 3},
            {'code': 'ICT002', 'name': 'Computer Applications II', 'description': 'Advanced computer applications and productivity tools', 'credits': 3},
            {'code': 'ICT003', 'name': 'Microsoft Word Processing', 'description': 'Word processing using Microsoft Word', 'credits': 2},
            {'code': 'ICT004', 'name': 'Microsoft Spreadsheets', 'description': 'Spreadsheet applications using Microsoft Excel', 'credits': 2},
            {'code': 'ICT005', 'name': 'Microsoft Database', 'description': 'Database management using Microsoft Access', 'credits': 2},
            {'code': 'ICT006', 'name': 'Microsoft PowerPoint', 'description': 'Presentation software using Microsoft PowerPoint', 'credits': 2},
            {'code': 'ICT007', 'name': 'Internet and Email', 'description': 'Internet browsing and email communication', 'credits': 2},
            {'code': 'ICT008', 'name': 'Computer Hardware and Maintenance', 'description': 'Basic computer hardware and troubleshooting', 'credits': 3},
            {'code': 'ICT009', 'name': 'Computer Networks', 'description': 'Introduction to computer networking', 'credits': 3},
            {'code': 'ICT010', 'name': 'Programming Fundamentals', 'description': 'Basic programming concepts and logic', 'credits': 3},
            {'code': 'ICT011', 'name': 'Web Design', 'description': 'Basic web design and HTML/CSS', 'credits': 3},
            {'code': 'ICT012', 'name': 'Digital Literacy', 'description': 'Digital skills and online safety', 'credits': 2}
        ],
        
        # Office Administration (OA101, OA102, OA103)
        'OA101': [
            {'code': 'OA001', 'name': 'Office Management', 'description': 'Principles of office management and administration', 'credits': 3},
            {'code': 'OA002', 'name': 'Business Communication', 'description': 'Effective business communication skills', 'credits': 3},
            {'code': 'OA003', 'name': 'Records Management', 'description': 'Document and records management systems', 'credits': 3},
            {'code': 'OA004', 'name': 'Customer Service', 'description': 'Customer service principles and practices', 'credits': 2},
            {'code': 'OA005', 'name': 'Business Law', 'description': 'Basic business law and regulations', 'credits': 3},
            {'code': 'OA006', 'name': 'Human Resource Management', 'description': 'Basic HR principles and practices', 'credits': 3},
            {'code': 'OA007', 'name': 'Project Management', 'description': 'Project planning and management', 'credits': 3},
            {'code': 'OA008', 'name': 'Financial Management', 'description': 'Basic financial management principles', 'credits': 3},
            {'code': 'OA009', 'name': 'Marketing Principles', 'description': 'Basic marketing concepts and strategies', 'credits': 3},
            {'code': 'OA010', 'name': 'Entrepreneurship', 'description': 'Entrepreneurial skills and business development', 'credits': 3}
        ],
        
        # Accountancy (ACC101)
        'ACC101': [
            {'code': 'ACC001', 'name': 'Financial Accounting I', 'description': 'Basic financial accounting principles', 'credits': 4},
            {'code': 'ACC002', 'name': 'Financial Accounting II', 'description': 'Advanced financial accounting concepts', 'credits': 4},
            {'code': 'ACC003', 'name': 'Cost Accounting', 'description': 'Cost accounting principles and methods', 'credits': 3},
            {'code': 'ACC004', 'name': 'Management Accounting', 'description': 'Management accounting for decision making', 'credits': 3},
            {'code': 'ACC005', 'name': 'Taxation', 'description': 'Kenyan tax laws and procedures', 'credits': 3},
            {'code': 'ACC006', 'name': 'Auditing', 'description': 'Auditing principles and procedures', 'credits': 3},
            {'code': 'ACC007', 'name': 'Business Law', 'description': 'Commercial law and regulations', 'credits': 3},
            {'code': 'ACC008', 'name': 'Economics', 'description': 'Basic economic principles', 'credits': 3},
            {'code': 'ACC009', 'name': 'Business Mathematics', 'description': 'Mathematical applications in business', 'credits': 3},
            {'code': 'ACC010', 'name': 'Computerized Accounting', 'description': 'Accounting software applications', 'credits': 3}
        ],
        
        # Supply Chain Management (SCM101, SCM102)
        'SCM101': [
            {'code': 'SCM001', 'name': 'Supply Chain Fundamentals', 'description': 'Introduction to supply chain management', 'credits': 3},
            {'code': 'SCM002', 'name': 'Procurement Management', 'description': 'Procurement principles and practices', 'credits': 3},
            {'code': 'SCM003', 'name': 'Inventory Management', 'description': 'Inventory control and management', 'credits': 3},
            {'code': 'SCM004', 'name': 'Warehouse Management', 'description': 'Warehouse operations and management', 'credits': 3},
            {'code': 'SCM005', 'name': 'Transportation Management', 'description': 'Transportation and logistics', 'credits': 3},
            {'code': 'SCM006', 'name': 'Supplier Management', 'description': 'Supplier relationship management', 'credits': 3},
            {'code': 'SCM007', 'name': 'Quality Management', 'description': 'Quality control and assurance', 'credits': 3},
            {'code': 'SCM008', 'name': 'Risk Management', 'description': 'Supply chain risk assessment and mitigation', 'credits': 3},
            {'code': 'SCM009', 'name': 'International Trade', 'description': 'International trade and customs', 'credits': 3},
            {'code': 'SCM010', 'name': 'Supply Chain Technology', 'description': 'Technology in supply chain management', 'credits': 3}
        ],
        
        # Business Management (BM101)
        'BM101': [
            {'code': 'BM001', 'name': 'Business Management Principles', 'description': 'Basic management principles and functions', 'credits': 3},
            {'code': 'BM002', 'name': 'Marketing Management', 'description': 'Marketing principles and strategies', 'credits': 3},
            {'code': 'BM003', 'name': 'Financial Management', 'description': 'Financial management for business', 'credits': 3},
            {'code': 'BM004', 'name': 'Human Resource Management', 'description': 'HR management principles', 'credits': 3},
            {'code': 'BM005', 'name': 'Operations Management', 'description': 'Business operations and processes', 'credits': 3},
            {'code': 'BM006', 'name': 'Business Communication', 'description': 'Effective business communication', 'credits': 2},
            {'code': 'BM007', 'name': 'Business Law', 'description': 'Legal aspects of business', 'credits': 3},
            {'code': 'BM008', 'name': 'Entrepreneurship', 'description': 'Entrepreneurial skills and business development', 'credits': 3}
        ],
        
        # Electrical Engineering (ELE101, ELE102, ELE103, ELE104)
        'ELE101': [
            {'code': 'ELE001', 'name': 'Electrical Principles', 'description': 'Basic electrical principles and theory', 'credits': 4},
            {'code': 'ELE002', 'name': 'Electrical Circuits', 'description': 'Electrical circuit analysis and design', 'credits': 4},
            {'code': 'ELE003', 'name': 'Electrical Machines', 'description': 'Electrical motors and generators', 'credits': 4},
            {'code': 'ELE004', 'name': 'Power Systems', 'description': 'Electrical power generation and distribution', 'credits': 4},
            {'code': 'ELE005', 'name': 'Electrical Installation', 'description': 'Electrical installation and wiring', 'credits': 4},
            {'code': 'ELE006', 'name': 'Electrical Maintenance', 'description': 'Electrical equipment maintenance', 'credits': 3},
            {'code': 'ELE007', 'name': 'Electrical Safety', 'description': 'Electrical safety practices and regulations', 'credits': 2},
            {'code': 'ELE008', 'name': 'Electronics', 'description': 'Basic electronics and components', 'credits': 3},
            {'code': 'ELE009', 'name': 'Control Systems', 'description': 'Electrical control systems', 'credits': 3},
            {'code': 'ELE010', 'name': 'Renewable Energy', 'description': 'Solar and renewable energy systems', 'credits': 3}
        ],
        
        # Fashion Design (FDM101, FD101, FD102)
        'FDM101': [
            {'code': 'FD001', 'name': 'Fashion Design Principles', 'description': 'Basic fashion design principles', 'credits': 3},
            {'code': 'FD002', 'name': 'Pattern Making', 'description': 'Pattern making and drafting', 'credits': 4},
            {'code': 'FD003', 'name': 'Garment Construction', 'description': 'Sewing and garment assembly', 'credits': 4},
            {'code': 'FD004', 'name': 'Fashion Illustration', 'description': 'Fashion drawing and illustration', 'credits': 3},
            {'code': 'FD005', 'name': 'Textile Science', 'description': 'Fabric properties and selection', 'credits': 3},
            {'code': 'FD006', 'name': 'Fashion History', 'description': 'History of fashion and trends', 'credits': 2},
            {'code': 'FD007', 'name': 'Fashion Marketing', 'description': 'Fashion business and marketing', 'credits': 3},
            {'code': 'FD008', 'name': 'Fashion Merchandising', 'description': 'Fashion retail and merchandising', 'credits': 3},
            {'code': 'FD009', 'name': 'Fashion Management', 'description': 'Fashion business management', 'credits': 3},
            {'code': 'FD010', 'name': 'Fashion Technology', 'description': 'Technology in fashion industry', 'credits': 3}
        ],
        
        # Automotive Technology (AT101, AT102)
        'AT101': [
            {'code': 'AT001', 'name': 'Automotive Fundamentals', 'description': 'Basic automotive principles', 'credits': 3},
            {'code': 'AT002', 'name': 'Engine Technology', 'description': 'Internal combustion engines', 'credits': 4},
            {'code': 'AT003', 'name': 'Transmission Systems', 'description': 'Manual and automatic transmissions', 'credits': 4},
            {'code': 'AT004', 'name': 'Brake Systems', 'description': 'Automotive brake systems', 'credits': 3},
            {'code': 'AT005', 'name': 'Suspension Systems', 'description': 'Vehicle suspension and steering', 'credits': 3},
            {'code': 'AT006', 'name': 'Electrical Systems', 'description': 'Automotive electrical systems', 'credits': 4},
            {'code': 'AT007', 'name': 'Fuel Systems', 'description': 'Fuel injection and carburetion', 'credits': 3},
            {'code': 'AT008', 'name': 'Diagnostic Systems', 'description': 'Vehicle diagnostics and troubleshooting', 'credits': 4},
            {'code': 'AT009', 'name': 'Auto Body Repair', 'description': 'Body repair and painting', 'credits': 3},
            {'code': 'AT010', 'name': 'Automotive Safety', 'description': 'Safety practices in automotive work', 'credits': 2}
        ],
        
        # Welding and Fabrication (WF101, WF102)
        'WF101': [
            {'code': 'WF001', 'name': 'Welding Fundamentals', 'description': 'Basic welding principles and safety', 'credits': 3},
            {'code': 'WF002', 'name': 'Arc Welding', 'description': 'Shielded metal arc welding (SMAW)', 'credits': 4},
            {'code': 'WF003', 'name': 'Gas Welding', 'description': 'Oxy-acetylene welding and cutting', 'credits': 3},
            {'code': 'WF004', 'name': 'MIG Welding', 'description': 'Gas metal arc welding (GMAW)', 'credits': 4},
            {'code': 'WF005', 'name': 'TIG Welding', 'description': 'Gas tungsten arc welding (GTAW)', 'credits': 4},
            {'code': 'WF006', 'name': 'Metal Fabrication', 'description': 'Metal cutting, forming and assembly', 'credits': 4},
            {'code': 'WF007', 'name': 'Blueprint Reading', 'description': 'Reading and interpreting blueprints', 'credits': 3},
            {'code': 'WF008', 'name': 'Quality Control', 'description': 'Welding quality control and inspection', 'credits': 3},
            {'code': 'WF009', 'name': 'Welding Metallurgy', 'description': 'Metallurgy and material properties', 'credits': 3},
            {'code': 'WF010', 'name': 'Advanced Welding', 'description': 'Specialized welding techniques', 'credits': 4}
        ],
        
        # Building Technology (BT101)
        'BT101': [
            {'code': 'BT001', 'name': 'Building Construction', 'description': 'Basic building construction methods', 'credits': 4},
            {'code': 'BT002', 'name': 'Building Materials', 'description': 'Construction materials and properties', 'credits': 3},
            {'code': 'BT003', 'name': 'Building Drawing', 'description': 'Architectural and structural drawings', 'credits': 3},
            {'code': 'BT004', 'name': 'Masonry', 'description': 'Brick and block laying techniques', 'credits': 4},
            {'code': 'BT005', 'name': 'Carpentry', 'description': 'Woodwork and joinery', 'credits': 4},
            {'code': 'BT006', 'name': 'Concrete Technology', 'description': 'Concrete mixing and placement', 'credits': 3},
            {'code': 'BT007', 'name': 'Building Services', 'description': 'Plumbing and electrical in buildings', 'credits': 3},
            {'code': 'BT008', 'name': 'Building Surveying', 'description': 'Building inspection and surveying', 'credits': 3},
            {'code': 'BT009', 'name': 'Building Management', 'description': 'Construction project management', 'credits': 3},
            {'code': 'BT010', 'name': 'Building Codes', 'description': 'Building regulations and standards', 'credits': 2}
        ],
        
        # Civil Engineering (CE101)
        'CE101': [
            {'code': 'CE001', 'name': 'Engineering Drawing', 'description': 'Technical drawing and CAD', 'credits': 3},
            {'code': 'CE002', 'name': 'Surveying', 'description': 'Land surveying and measurements', 'credits': 4},
            {'code': 'CE003', 'name': 'Soil Mechanics', 'description': 'Soil properties and testing', 'credits': 4},
            {'code': 'CE004', 'name': 'Structural Analysis', 'description': 'Structural analysis and design', 'credits': 4},
            {'code': 'CE005', 'name': 'Highway Engineering', 'description': 'Road design and construction', 'credits': 3},
            {'code': 'CE006', 'name': 'Water Resources', 'description': 'Water supply and drainage', 'credits': 3},
            {'code': 'CE007', 'name': 'Construction Management', 'description': 'Construction project management', 'credits': 3},
            {'code': 'CE008', 'name': 'Environmental Engineering', 'description': 'Environmental impact assessment', 'credits': 3},
            {'code': 'CE009', 'name': 'Transportation Engineering', 'description': 'Transportation planning and design', 'credits': 3},
            {'code': 'CE010', 'name': 'Geotechnical Engineering', 'description': 'Foundation design and soil engineering', 'credits': 4}
        ],
        
        # Plumbing (PL101, PL102)
        'PL101': [
            {'code': 'PL001', 'name': 'Plumbing Fundamentals', 'description': 'Basic plumbing principles and tools', 'credits': 3},
            {'code': 'PL002', 'name': 'Water Supply Systems', 'description': 'Water supply installation and maintenance', 'credits': 4},
            {'code': 'PL003', 'name': 'Drainage Systems', 'description': 'Waste water and drainage systems', 'credits': 4},
            {'code': 'PL004', 'name': 'Pipe Fitting', 'description': 'Pipe installation and jointing', 'credits': 4},
            {'code': 'PL005', 'name': 'Plumbing Fixtures', 'description': 'Installation of plumbing fixtures', 'credits': 3},
            {'code': 'PL006', 'name': 'Plumbing Codes', 'description': 'Plumbing regulations and standards', 'credits': 2},
            {'code': 'PL007', 'name': 'Plumbing Maintenance', 'description': 'Plumbing system maintenance', 'credits': 3},
            {'code': 'PL008', 'name': 'Gas Fitting', 'description': 'Gas installation and safety', 'credits': 3},
            {'code': 'PL009', 'name': 'Solar Water Heating', 'description': 'Solar water heating systems', 'credits': 3},
            {'code': 'PL010', 'name': 'Plumbing Design', 'description': 'Plumbing system design', 'credits': 3}
        ],
        
        # Food Production (FBP101, FP101, FP102, FP103)
        'FBP101': [
            {'code': 'FP001', 'name': 'Food Safety and Hygiene', 'description': 'Food safety principles and practices', 'credits': 3},
            {'code': 'FP002', 'name': 'Food Preparation', 'description': 'Basic food preparation techniques', 'credits': 4},
            {'code': 'FP003', 'name': 'Culinary Arts', 'description': 'Advanced cooking techniques', 'credits': 4},
            {'code': 'FP004', 'name': 'Bakery and Pastry', 'description': 'Baking and pastry making', 'credits': 4},
            {'code': 'FP005', 'name': 'Menu Planning', 'description': 'Menu development and planning', 'credits': 3},
            {'code': 'FP006', 'name': 'Food Costing', 'description': 'Food cost control and pricing', 'credits': 3},
            {'code': 'FP007', 'name': 'Kitchen Management', 'description': 'Kitchen operations and management', 'credits': 3},
            {'code': 'FP008', 'name': 'Nutrition', 'description': 'Basic nutrition principles', 'credits': 3},
            {'code': 'FP009', 'name': 'International Cuisine', 'description': 'World cuisines and cooking styles', 'credits': 3},
            {'code': 'FP010', 'name': 'Food Service', 'description': 'Food service operations', 'credits': 3}
        ],
        
        # Agriculture (AEXT101, SARD101, AEXT102)
        'AEXT101': [
            {'code': 'AG001', 'name': 'Agricultural Principles', 'description': 'Basic agricultural principles', 'credits': 3},
            {'code': 'AG002', 'name': 'Crop Production', 'description': 'Crop cultivation and management', 'credits': 4},
            {'code': 'AG003', 'name': 'Animal Husbandry', 'description': 'Livestock management and care', 'credits': 4},
            {'code': 'AG004', 'name': 'Soil Science', 'description': 'Soil properties and management', 'credits': 3},
            {'code': 'AG005', 'name': 'Agricultural Extension', 'description': 'Extension services and rural development', 'credits': 3},
            {'code': 'AG006', 'name': 'Agricultural Economics', 'description': 'Agricultural business and economics', 'credits': 3},
            {'code': 'AG007', 'name': 'Agricultural Technology', 'description': 'Modern agricultural technology', 'credits': 3},
            {'code': 'AG008', 'name': 'Sustainable Agriculture', 'description': 'Sustainable farming practices', 'credits': 3},
            {'code': 'AG009', 'name': 'Agricultural Marketing', 'description': 'Agricultural marketing and value chains', 'credits': 3},
            {'code': 'AG010', 'name': 'Agricultural Policy', 'description': 'Agricultural policies and regulations', 'credits': 2}
        ],
        
        # Social Work (SW101, SW102)
        'SW101': [
            {'code': 'SW001', 'name': 'Social Work Principles', 'description': 'Basic social work principles and ethics', 'credits': 3},
            {'code': 'SW002', 'name': 'Human Behavior', 'description': 'Human behavior and social environment', 'credits': 3},
            {'code': 'SW003', 'name': 'Social Policy', 'description': 'Social policy and welfare systems', 'credits': 3},
            {'code': 'SW004', 'name': 'Community Development', 'description': 'Community development principles', 'credits': 4},
            {'code': 'SW005', 'name': 'Case Management', 'description': 'Social work case management', 'credits': 3},
            {'code': 'SW006', 'name': 'Counseling Skills', 'description': 'Basic counseling techniques', 'credits': 3},
            {'code': 'SW007', 'name': 'Group Work', 'description': 'Social group work methods', 'credits': 3},
            {'code': 'SW008', 'name': 'Research Methods', 'description': 'Social work research methods', 'credits': 3},
            {'code': 'SW009', 'name': 'Social Work Practice', 'description': 'Field practice and supervision', 'credits': 4},
            {'code': 'SW010', 'name': 'Social Justice', 'description': 'Social justice and human rights', 'credits': 3}
        ],
        
        # Food Technology (FT101, FT102)
        'FT101': [
            {'code': 'FT001', 'name': 'Food Chemistry', 'description': 'Chemical composition of foods', 'credits': 4},
            {'code': 'FT002', 'name': 'Food Microbiology', 'description': 'Microbiology in food processing', 'credits': 4},
            {'code': 'FT003', 'name': 'Food Processing', 'description': 'Food processing and preservation', 'credits': 4},
            {'code': 'FT004', 'name': 'Food Safety', 'description': 'Food safety and quality assurance', 'credits': 3},
            {'code': 'FT005', 'name': 'Food Analysis', 'description': 'Food analysis and testing methods', 'credits': 4},
            {'code': 'FT006', 'name': 'Food Packaging', 'description': 'Food packaging technology', 'credits': 3},
            {'code': 'FT007', 'name': 'Food Engineering', 'description': 'Food processing equipment and technology', 'credits': 4},
            {'code': 'FT008', 'name': 'Food Regulations', 'description': 'Food laws and regulations', 'credits': 2},
            {'code': 'FT009', 'name': 'Food Product Development', 'description': 'New food product development', 'credits': 3},
            {'code': 'FT010', 'name': 'Food Industry Management', 'description': 'Food industry operations management', 'credits': 3}
        ],
        
        # Science Laboratory Technology (SLT101, SLT102)
        'SLT101': [
            {'code': 'SLT001', 'name': 'Laboratory Safety', 'description': 'Laboratory safety and procedures', 'credits': 2},
            {'code': 'SLT002', 'name': 'Analytical Chemistry', 'description': 'Chemical analysis techniques', 'credits': 4},
            {'code': 'SLT003', 'name': 'Microbiology', 'description': 'Microbiological techniques', 'credits': 4},
            {'code': 'SLT004', 'name': 'Biochemistry', 'description': 'Biochemical analysis methods', 'credits': 4},
            {'code': 'SLT005', 'name': 'Instrumentation', 'description': 'Laboratory instruments and equipment', 'credits': 3},
            {'code': 'SLT006', 'name': 'Quality Control', 'description': 'Quality control in laboratories', 'credits': 3},
            {'code': 'SLT007', 'name': 'Environmental Analysis', 'description': 'Environmental testing methods', 'credits': 3},
            {'code': 'SLT008', 'name': 'Food Analysis', 'description': 'Food testing and analysis', 'credits': 3},
            {'code': 'SLT009', 'name': 'Laboratory Management', 'description': 'Laboratory operations management', 'credits': 3},
            {'code': 'SLT010', 'name': 'Research Methods', 'description': 'Scientific research methods', 'credits': 3}
        ],
        
        # Library and Information Science (LIS101, LIS102)
        'LIS101': [
            {'code': 'LIS001', 'name': 'Library Science Fundamentals', 'description': 'Basic library science principles', 'credits': 3},
            {'code': 'LIS002', 'name': 'Information Organization', 'description': 'Cataloging and classification', 'credits': 4},
            {'code': 'LIS003', 'name': 'Information Retrieval', 'description': 'Information search and retrieval', 'credits': 3},
            {'code': 'LIS004', 'name': 'Reference Services', 'description': 'Reference and information services', 'credits': 3},
            {'code': 'LIS005', 'name': 'Collection Development', 'description': 'Library collection management', 'credits': 3},
            {'code': 'LIS006', 'name': 'Digital Libraries', 'description': 'Digital library systems', 'credits': 3},
            {'code': 'LIS007', 'name': 'Information Technology', 'description': 'IT applications in libraries', 'credits': 3},
            {'code': 'LIS008', 'name': 'Library Management', 'description': 'Library administration and management', 'credits': 3},
            {'code': 'LIS009', 'name': 'Information Literacy', 'description': 'Information literacy instruction', 'credits': 3},
            {'code': 'LIS010', 'name': 'Archives Management', 'description': 'Archives and records management', 'credits': 3}
        ]
    }
    
    return units_data 