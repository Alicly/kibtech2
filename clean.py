from app import db
from sqlalchemy import text

# Try to import create_app if using an app factory
try:
    from app import create_app
    app = create_app()
except ImportError:
    app = None

def cleanup_all_student_course_duplicates():
    print("Checking for duplicate enrollments...")
    result = db.session.execute(text('''
        SELECT student_id, course_id, COUNT(*) as cnt
        FROM student_course_enrollments
        GROUP BY student_id, course_id
        HAVING cnt > 1
    '''))
    duplicates = result.fetchall()
    if not duplicates:
        print('No duplicates found.')
        return
    for student_id, course_id, cnt in duplicates:
        db.session.execute(
            text('''
                DELETE FROM student_course_enrollments
                WHERE rowid NOT IN (
                    SELECT MIN(rowid)
                    FROM student_course_enrollments
                    WHERE student_id = :sid AND course_id = :cid
                )
                AND student_id = :sid AND course_id = :cid
            '''), {'sid': student_id, 'cid': course_id}
        )
    db.session.commit()
    print('Duplicate enrollments cleaned up!')

if __name__ == '__main__':
    if app:
        with app.app_context():
            cleanup_all_student_course_duplicates()
    else:
        cleanup_all_student_course_duplicates()