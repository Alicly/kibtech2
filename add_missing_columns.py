from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Add missing columns to courses table
        db.session.execute(text('ALTER TABLE courses ADD COLUMN entry_requirements VARCHAR(200)'))
        print("Added entry_requirements column")
        
        db.session.execute(text('ALTER TABLE courses ADD COLUMN exam_body VARCHAR(50)'))
        print("Added exam_body column")
        
        db.session.commit()
        print("Successfully added missing columns to courses table")
    except Exception as e:
        db.session.rollback()
        print(f"Error (courses): {str(e)}")
        # Check if columns already exist
        try:
            result = db.session.execute(text("PRAGMA table_info(courses)"))
            columns = [row[1] for row in result]
            print(f"Existing columns in courses: {columns}")
        except Exception as e2:
            print(f"Error checking columns (courses): {str(e2)}")

    try:
        # Add missing lecturer_id column to class_rooms table
        db.session.execute(text('ALTER TABLE class_rooms ADD COLUMN lecturer_id INTEGER'))
        db.session.commit()
        print("Added lecturer_id column to class_rooms")
    except Exception as e:
        db.session.rollback()
        print(f"Error (class_rooms): {str(e)}")
        try:
            result = db.session.execute(text("PRAGMA table_info(class_rooms)"))
            columns = [row[1] for row in result]
            print(f"Existing columns in class_rooms: {columns}")
        except Exception as e2:
            print(f"Error checking columns (class_rooms): {str(e2)}")

    try:
        # Add missing day column to class_rooms table
        db.session.execute(text('ALTER TABLE class_rooms ADD COLUMN day VARCHAR(20)'))
        db.session.commit()
        print("Added day column to class_rooms")
    except Exception as e:
        db.session.rollback()
        print(f"Error (class_rooms.day): {str(e)}")
        try:
            result = db.session.execute(text("PRAGMA table_info(class_rooms)"))
            columns = [row[1] for row in result]
            print(f"Existing columns in class_rooms: {columns}")
        except Exception as e2:
            print(f"Error checking columns (class_rooms): {str(e2)}")

    try:
        # Add missing start_time column to class_rooms table
        db.session.execute(text('ALTER TABLE class_rooms ADD COLUMN start_time TIME'))
        db.session.commit()
        print("Added start_time column to class_rooms")
    except Exception as e:
        db.session.rollback()
        print(f"Error (class_rooms.start_time): {str(e)}")
        try:
            result = db.session.execute(text("PRAGMA table_info(class_rooms)"))
            columns = [row[1] for row in result]
            print(f"Existing columns in class_rooms: {columns}")
        except Exception as e2:
            print(f"Error checking columns (class_rooms): {str(e2)}")

    try:
        # Add missing end_time column to class_rooms table
        db.session.execute(text('ALTER TABLE class_rooms ADD COLUMN end_time TIME'))
        db.session.commit()
        print("Added end_time column to class_rooms")
    except Exception as e:
        db.session.rollback()
        print(f"Error (class_rooms.end_time): {str(e)}")
        try:
            result = db.session.execute(text("PRAGMA table_info(class_rooms)"))
            columns = [row[1] for row in result]
            print(f"Existing columns in class_rooms: {columns}")
        except Exception as e2:
            print(f"Error checking columns (class_rooms): {str(e2)}")

    try:
        # Add missing capacity column to class_rooms table
        db.session.execute(text('ALTER TABLE class_rooms ADD COLUMN capacity INTEGER'))
        db.session.commit()
        print("Added capacity column to class_rooms")
    except Exception as e:
        db.session.rollback()
        print(f"Error (class_rooms.capacity): {str(e)}")
        try:
            result = db.session.execute(text("PRAGMA table_info(class_rooms)"))
            columns = [row[1] for row in result]
            print(f"Existing columns in class_rooms: {columns}")
        except Exception as e2:
            print(f"Error checking columns (class_rooms): {str(e2)}")

    # Add missing columns to users table
    try:
        # Add missing registration_number column to users table
        db.session.execute(text('ALTER TABLE users ADD COLUMN registration_number VARCHAR(50)'))
        db.session.commit()
        print("Added registration_number column to users")
    except Exception as e:
        db.session.rollback()
        print(f"Error (users.registration_number): {str(e)}")

    try:
        # Add missing course_id column to users table
        db.session.execute(text('ALTER TABLE users ADD COLUMN course_id INTEGER'))
        db.session.commit()
        print("Added course_id column to users")
    except Exception as e:
        db.session.rollback()
        print(f"Error (users.course_id): {str(e)}")

    try:
        # Add missing lecturer_id column to users table
        db.session.execute(text('ALTER TABLE users ADD COLUMN lecturer_id INTEGER'))
        db.session.commit()
        print("Added lecturer_id column to users")
    except Exception as e:
        db.session.rollback()
        print(f"Error (users.lecturer_id): {str(e)}")

    try:
        # Add missing department column to users table
        db.session.execute(text('ALTER TABLE users ADD COLUMN department VARCHAR(100)'))
        db.session.commit()
        print("Added department column to users")
    except Exception as e:
        db.session.rollback()
        print(f"Error (users.department): {str(e)}")

    try:
        # Add missing specialization column to users table
        db.session.execute(text('ALTER TABLE users ADD COLUMN specialization VARCHAR(100)'))
        db.session.commit()
        print("Added specialization column to users")
    except Exception as e:
        db.session.rollback()
        print(f"Error (users.specialization): {str(e)}")

    try:
        # Add missing staff_id column to users table
        db.session.execute(text('ALTER TABLE users ADD COLUMN staff_id VARCHAR(50)'))
        db.session.commit()
        print("Added staff_id column to users")
    except Exception as e:
        db.session.rollback()
        print(f"Error (users.staff_id): {str(e)}")

    try:
        # Add missing position column to users table
        db.session.execute(text('ALTER TABLE users ADD COLUMN position VARCHAR(100)'))
        db.session.commit()
        print("Added position column to users")
    except Exception as e:
        db.session.rollback()
        print(f"Error (users.position): {str(e)}")

    # Check final state of users table
    try:
        result = db.session.execute(text("PRAGMA table_info(users)"))
        columns = [row[1] for row in result]
        print(f"Final columns in users table: {columns}")
    except Exception as e:
        print(f"Error checking final users columns: {str(e)}") 