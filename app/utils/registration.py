from datetime import datetime
from app.models import Course

class RegistrationNumberGenerator:
    # Course prefixes mapping
    COURSE_PREFIXES = {
        'electrical_installation': 'EI',
        'plumbing': 'PL',
        'welding': 'WD',
        'carpentry': 'CP',
        'masonry': 'MS',
        'electrical_engineering': 'EE',
        'building_technology': 'BT',
        'mechanical_engineering': 'ME',
        'civil_engineering': 'CE'
    }

    @staticmethod
    def generate_registration_number(course_code, year=None):
        """
        Generate a registration number in the format: KTT/COURSE/YEAR/NUMBER
        
        Example: KTT/EI/2024/001 for Electrical Installation student in 2024
        """
        if year is None:
            year = datetime.now().year

        # Get the course prefix
        course_prefix = RegistrationNumberGenerator.COURSE_PREFIXES.get(course_code.lower())
        if not course_prefix:
            raise ValueError(f"Invalid course code: {course_code}")

        # Get the last registration number for this course and year
        last_reg = RegistrationNumberGenerator.get_last_registration_number(course_prefix, year)
        
        # Generate new number
        if last_reg:
            # Extract the number part and increment
            number = int(last_reg.split('/')[-1]) + 1
        else:
            number = 1

        # Format the registration number
        reg_number = f"KTT/{course_prefix}/{year}/{number:03d}"
        return reg_number

    @staticmethod
    def get_last_registration_number(course_prefix, year):
        """
        Get the last registration number for a given course and year
        This would typically query the database
        """
        # This is a placeholder - in a real application, you would query the database
        # Example: return User.query.filter(User.registration_number.like(f"KTT/{course_prefix}/{year}/%")).order_by(User.registration_number.desc()).first()
        return None

    @staticmethod
    def validate_registration_number(reg_number):
        """
        Validate a registration number format
        """
        try:
            parts = reg_number.split('/')
            if len(parts) != 4:
                return False
            
            prefix, course, year, number = parts
            
            # Check prefix
            if prefix != 'KTT':
                return False
                
            # Check course code
            if course not in RegistrationNumberGenerator.COURSE_PREFIXES.values():
                return False
                
            # Check year
            if not year.isdigit() or len(year) != 4:
                return False
                
            # Check number
            if not number.isdigit() or len(number) != 3:
                return False
                
            return True
        except:
            return False

    @staticmethod
    def get_course_from_registration(reg_number):
        """
        Extract course information from registration number
        """
        if not RegistrationNumberGenerator.validate_registration_number(reg_number):
            return None
            
        parts = reg_number.split('/')
        course_code = parts[1]
        
        # Reverse lookup course name from prefix
        for course, prefix in RegistrationNumberGenerator.COURSE_PREFIXES.items():
            if prefix == course_code:
                return course
                
        return None 