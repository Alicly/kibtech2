from app import create_app, db
from app.models.course import Course
from app.models.unit import Unit
from app.data.units import create_units
from datetime import datetime

# Fallback generic units
GENERIC_UNITS = [
    {'code': 'GEN001', 'name': 'Communication Skills', 'description': 'Effective communication in the workplace', 'credits': 2},
    {'code': 'GEN002', 'name': 'Entrepreneurship', 'description': 'Entrepreneurial skills and business development', 'credits': 2},
    {'code': 'GEN003', 'name': 'ICT Basics', 'description': 'Basic computer and digital skills', 'credits': 2},
    {'code': 'GEN004', 'name': 'Occupational Safety', 'description': 'Workplace safety and health', 'credits': 2},
    {'code': 'GEN005', 'name': 'Professional Ethics', 'description': 'Ethical conduct in the profession', 'credits': 2},
]

def best_unit_set(course, units_data):
    cname = course.name.lower()
    ccat = (course.category or '').lower()
    ccode = course.code.upper()
    # Try direct code match
    if ccode in units_data:
        return units_data[ccode]
    # Try partial code match
    for key in units_data:
        if key in ccode:
            return units_data[key]
    # Try by keywords in name/category
    if 'ict' in cname or 'information technology' in cname or 'ict' in ccat:
        return units_data.get('ICT101') or GENERIC_UNITS
    if 'electrical' in cname or 'electrical' in ccat:
        return units_data.get('ELE101') or GENERIC_UNITS
    if 'fashion' in cname or 'garment' in cname or 'fashion' in ccat:
        return units_data.get('FD101') or GENERIC_UNITS
    if 'building' in cname or 'building' in ccat:
        return units_data.get('BT101') or GENERIC_UNITS
    if 'business' in cname or 'business' in ccat:
        return units_data.get('BM101') or GENERIC_UNITS
    if 'hospitality' in cname or 'food' in cname or 'culinary' in cname or 'hospitality' in ccat:
        return units_data.get('FBP101') or GENERIC_UNITS
    if 'mechanical' in cname or 'mechanical' in ccat:
        return units_data.get('MEC101') or GENERIC_UNITS
    if 'civil' in cname or 'civil' in ccat:
        return units_data.get('CE101') or GENERIC_UNITS
    if 'plumbing' in cname or 'plumbing' in ccat:
        return units_data.get('PL101') or GENERIC_UNITS
    if 'welding' in cname or 'fabrication' in cname:
        return units_data.get('WF101') or GENERIC_UNITS
    if 'account' in cname:
        return units_data.get('ACC101') or GENERIC_UNITS
    if 'supply chain' in cname:
        return units_data.get('SCM101') or GENERIC_UNITS
    if 'office' in cname:
        return units_data.get('BM101') or GENERIC_UNITS
    if 'agricultur' in cname:
        return units_data.get('AEXT101') or GENERIC_UNITS
    # Fallback
    return GENERIC_UNITS

def add_missing_units():
    app = create_app()
    with app.app_context():
        units_data = create_units()
        courses = Course.query.all()
        added = 0
        for course in courses:
            if course.units.count() == 0:
                unit_set = best_unit_set(course, units_data)
                for u in unit_set:
                    unit = Unit(
                        code=u['code'],
                        name=u['name'],
                        description=u.get('description'),
                        credits=u.get('credits'),
                        course_id=course.id,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                    )
                    db.session.add(unit)
                print(f"Added {len(unit_set)} units to course: {course.code} - {course.name}")
                added += 1
        db.session.commit()
        print(f"\nDone. Updated {added} courses.")

if __name__ == "__main__":
    add_missing_units() 