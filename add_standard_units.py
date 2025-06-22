from app import create_app, db
from app.models.course import Course
from app.models.unit import Unit

# Standard units for Certificate in Information Technology (CIT)
CIT_UNITS = [
    ("CIT101", "Introduction to Information Communication Technology"),
    ("CIT102", "Computer Applications (Practical)"),
    ("CIT103", "Basic Electronics"),
    ("CIT104", "Mathematics"),
    ("CIT105", "Communication Skills"),
    ("CIT106", "Operating Systems"),
    ("CIT107", "Entrepreneurship Education"),
    ("CIT108", "Computer Maintenance & Support"),
    ("CIT109", "Computer Applications II (Theory)"),
    ("CIT110", "Computer Applications II (Practical)"),
    ("CIT111", "Structured Programming"),
    ("CIT112", "Course Specialization Project"),
]

EEE_UNITS = [
    ("EEE101", "Electrical Principles"),
    ("EEE102", "Workshop Technology"),
    ("EEE103", "Electrical Installation Technology"),
    ("EEE104", "Engineering Mathematics"),
    ("EEE105", "Technical Drawing"),
    ("EEE106", "Communication Skills"),
    ("EEE107", "Entrepreneurship Education"),
    ("EEE108", "Estimating and Costing"),
    ("EEE109", "Electronics"),
    ("EEE110", "Industrial Organization & Management"),
    ("EEE111", "ICT for Engineers"),
]

FDG_UNITS = [
    ("FDG101", "Elements of Fashion Design"),
    ("FDG102", "Textile Science"),
    ("FDG103", "Pattern Drafting"),
    ("FDG104", "Garment Construction"),
    ("FDG105", "Fashion Illustration"),
    ("FDG106", "Entrepreneurship Education"),
    ("FDG107", "Communication Skills"),
    ("FDG108", "ICT for Fashion"),
    ("FDG109", "Industrial Attachment"),
]

BLD_UNITS = [
    ("BLD101", "Building Construction"),
    ("BLD102", "Construction Materials"),
    ("BLD103", "Technical Drawing"),
    ("BLD104", "Mathematics"),
    ("BLD105", "Workshop Practice"),
    ("BLD106", "Entrepreneurship Education"),
    ("BLD107", "Communication Skills"),
    ("BLD108", "Site Management"),
    ("BLD109", "ICT for Building"),
]

BMT_UNITS = [
    ("BMT101", "Principles of Business Management"),
    ("BMT102", "Business Law"),
    ("BMT103", "Business Communication"),
    ("BMT104", "Economics"),
    ("BMT105", "ICT for Business"),
    ("BMT106", "Entrepreneurship Education"),
    ("BMT107", "Financial Accounting"),
    ("BMT108", "Marketing"),
    ("BMT109", "Office Administration"),
]

HOS_UNITS = [
    ("HOS101", "Food Production"),
    ("HOS102", "Food & Beverage Service"),
    ("HOS103", "Housekeeping Operations"),
    ("HOS104", "Front Office Operations"),
    ("HOS105", "Nutrition"),
    ("HOS106", "Communication Skills"),
    ("HOS107", "Entrepreneurship Education"),
    ("HOS108", "ICT for Hospitality"),
    ("HOS109", "Catering & Event Management"),
]

MEC_UNITS = [
    ("MEC101", "Engineering Mathematics"),
    ("MEC102", "Engineering Drawing"),
    ("MEC103", "Workshop Technology"),
    ("MEC104", "Mechanics of Machines"),
    ("MEC105", "Thermodynamics"),
    ("MEC106", "Communication Skills"),
    ("MEC107", "Entrepreneurship Education"),
    ("MEC108", "Industrial Organization & Management"),
    ("MEC109", "ICT for Engineers"),
]

COURSE_UNITS_MAP = {
    "Certificate in Information Technology": CIT_UNITS,
    "Certificate in Electrical Engineering": EEE_UNITS,
    "Certificate in Fashion Design & Garment Making": FDG_UNITS,
    "Certificate in Building Technology": BLD_UNITS,
    "Certificate in Business Management": BMT_UNITS,
    "Certificate in Hospitality Management": HOS_UNITS,
    "Certificate in Mechanical Engineering": MEC_UNITS,
}

def add_units_to_courses():
    app = create_app()
    with app.app_context():
        courses = Course.query.all()
        added_count = 0
        for course in courses:
            if course.units.count() == 0:
                # Try to match by exact name, or by keywords in name/category
                units = COURSE_UNITS_MAP.get(course.name)
                if not units:
                    # Try matching by category or partial name
                    cname = course.name.lower()
                    ccat = (course.category or '').lower()
                    if 'ict' in cname or 'information technology' in cname or 'ict' in ccat:
                        units = CIT_UNITS
                    elif 'electrical' in cname or 'electrical' in ccat:
                        units = EEE_UNITS
                    elif 'fashion' in cname or 'garment' in cname or 'fashion' in ccat:
                        units = FDG_UNITS
                    elif 'building' in cname or 'building' in ccat:
                        units = BLD_UNITS
                    elif 'business' in cname or 'business' in ccat:
                        units = BMT_UNITS
                    elif 'hospitality' in cname or 'hospitality' in ccat:
                        units = HOS_UNITS
                    elif 'mechanical' in cname or 'mechanical' in ccat:
                        units = MEC_UNITS
                if units:
                    for code, name in units:
                        unit = Unit(code=code, name=name, course_id=course.id)
                        db.session.add(unit)
                    print(f"Added {len(units)} units to course: {course.name}")
                    added_count += 1
        db.session.commit()
        print(f"Done. Updated {added_count} courses.")

if __name__ == "__main__":
    add_units_to_courses() 