import psycopg2
from psycopg2 import sql
from app import create_app, db
from sqlalchemy import text
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import Config
import re

# Update these with your actual DB credentials if needed
DB_NAME = 'railway'
DB_USER = 'postgres'
DB_PASSWORD = 'boPZoFfrLgZYgBHqqBmfvXHSKnENLLKg'
DB_HOST = 'mainline.proxy.rlwy.net'
DB_PORT = '59135'

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

# Check if lecturer_id column exists
cur.execute("""
SELECT column_name FROM information_schema.columns WHERE table_name='class_rooms' AND column_name='lecturer_id';
""")
exists = cur.fetchone()

if not exists:
    print('Adding lecturer_id column to class_rooms...')
    cur.execute("""
    ALTER TABLE class_rooms ADD COLUMN lecturer_id INTEGER REFERENCES users(id);
    """)
    conn.commit()
    print('lecturer_id column added.')
else:
    print('lecturer_id column already exists.')

# Add day column
cur.execute("""
ALTER TABLE class_rooms 
ADD COLUMN IF NOT EXISTS day VARCHAR(10)
""")

# Add start_time column
cur.execute("""
ALTER TABLE class_rooms 
ADD COLUMN IF NOT EXISTS start_time TIME
""")

# Add end_time column
cur.execute("""
ALTER TABLE class_rooms 
ADD COLUMN IF NOT EXISTS end_time TIME
""")

conn.commit()
print('Schema check complete.')

app = create_app()

with app.app_context():
    try:
        # Add day column
        db.session.execute(text("""
            ALTER TABLE class_rooms 
            ADD COLUMN IF NOT EXISTS day VARCHAR(10)
        """))
        
        # Add start_time column
        db.session.execute(text("""
            ALTER TABLE class_rooms 
            ADD COLUMN IF NOT EXISTS start_time TIME
        """))
        
        # Add end_time column
        db.session.execute(text("""
            ALTER TABLE class_rooms 
            ADD COLUMN IF NOT EXISTS end_time TIME
        """))
        
        # Add capacity column to class_rooms table if it doesn't exist
        db.session.execute(text("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'class_rooms' 
                    AND column_name = 'capacity'
                ) THEN
                    ALTER TABLE class_rooms 
                    ADD COLUMN capacity INTEGER NOT NULL DEFAULT 30;
                END IF;
            END $$;
        """))
        
        # Add created_at and updated_at columns to grades table if they don't exist
        db.session.execute(text("""
            DO $$ 
            BEGIN 
                IF NOT EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'grades' 
                    AND column_name = 'created_at'
                ) THEN
                    ALTER TABLE grades 
                    ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                END IF;
                
                IF NOT EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'grades' 
                    AND column_name = 'updated_at'
                ) THEN
                    ALTER TABLE grades 
                    ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                END IF;
            END $$;
        """))
        
        # Alter start_time and end_time columns in class_rooms table
        db.session.execute(text("""
            DO $$
            BEGIN
                -- Check if columns exist and are of type TIME
                IF EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name = 'class_rooms' 
                          AND column_name = 'start_time' 
                          AND data_type = 'time without time zone') THEN
                    -- Convert TIME to TIMESTAMP
                    ALTER TABLE class_rooms 
                    ALTER COLUMN start_time TYPE TIMESTAMP 
                    USING (CURRENT_DATE + start_time);
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name = 'class_rooms' 
                          AND column_name = 'end_time' 
                          AND data_type = 'time without time zone') THEN
                    -- Convert TIME to TIMESTAMP
                    ALTER TABLE class_rooms 
                    ALTER COLUMN end_time TYPE TIMESTAMP 
                    USING (CURRENT_DATE + end_time);
                END IF;
            END $$;
        """))
        
        db.session.commit()
        print("Successfully added day, start_time, end_time, and capacity columns to class_rooms table")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")

cur.close()
conn.close()

def extract_db_info(uri):
    # Extract database name from URI
    db_name = re.search(r'/([^/?]+)(?:\?|$)', uri)
    if db_name:
        return db_name.group(1)
    return None

def reset_database():
    # Extract database name from URI
    db_name = extract_db_info(Config.SQLALCHEMY_DATABASE_URI)
    if not db_name:
        print("Could not extract database name from URI")
        return

    # Connect to default database to drop and recreate
    conn = psycopg2.connect(
        host="mainline.proxy.rlwy.net",
        port="59135",
        user="postgres",
        password="boPZoFfrLgZYgBHqqBmfvXHSKnENLLKg",
        database="railway"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    try:
        # Drop existing database if it exists
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        print(f"Database {db_name} dropped successfully")

        # Create new database
        cur.execute(f"CREATE DATABASE {db_name}")
        print(f"Database {db_name} created successfully")

    except Exception as e:
        print(f"Error during database reset: {str(e)}")
    finally:
        cur.close()
        conn.close()

    # Connect to the new database to create tables
    conn = psycopg2.connect(Config.SQLALCHEMY_DATABASE_URI)
    cur = conn.cursor()

    try:
        # Create tables
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(128),
                role VARCHAR(20) NOT NULL,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(20) UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS class_rooms (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                course_id INTEGER REFERENCES courses(id),
                lecturer_id INTEGER REFERENCES users(id),
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                day VARCHAR(10) NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                capacity INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS class_enrollments (
                student_id INTEGER REFERENCES users(id),
                class_id INTEGER REFERENCES class_rooms(id),
                PRIMARY KEY (student_id, class_id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                class_id INTEGER REFERENCES class_rooms(id),
                due_date TIMESTAMP NOT NULL,
                total_points INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id SERIAL PRIMARY KEY,
                assignment_id INTEGER REFERENCES assignments(id),
                student_id INTEGER REFERENCES users(id),
                content TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                grade INTEGER,
                feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id SERIAL PRIMARY KEY,
                class_id INTEGER REFERENCES class_rooms(id),
                student_id INTEGER REFERENCES users(id),
                date DATE NOT NULL,
                status VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS teaching_materials (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                file_path VARCHAR(255),
                class_id INTEGER REFERENCES class_rooms(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                id SERIAL PRIMARY KEY,
                student_id INTEGER REFERENCES users(id),
                class_id INTEGER REFERENCES class_rooms(id),
                assignment_id INTEGER REFERENCES assignments(id),
                score INTEGER NOT NULL,
                feedback TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Add created_at and updated_at columns to grades table if they don't exist
        cur.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                             WHERE table_name = 'grades' AND column_name = 'created_at') THEN
                    ALTER TABLE grades ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                END IF;
                
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                             WHERE table_name = 'grades' AND column_name = 'updated_at') THEN
                    ALTER TABLE grades ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                END IF;
            END $$;
        """)

        # Alter start_time and end_time columns in class_rooms table
        cur.execute("""
            DO $$
            BEGIN
                -- Check if columns exist and are of type TIME
                IF EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name = 'class_rooms' 
                          AND column_name = 'start_time' 
                          AND data_type = 'time without time zone') THEN
                    -- Convert TIME to TIMESTAMP
                    ALTER TABLE class_rooms 
                    ALTER COLUMN start_time TYPE TIMESTAMP 
                    USING (CURRENT_DATE + start_time);
                END IF;

                IF EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name = 'class_rooms' 
                          AND column_name = 'end_time' 
                          AND data_type = 'time without time zone') THEN
                    -- Convert TIME to TIMESTAMP
                    ALTER TABLE class_rooms 
                    ALTER COLUMN end_time TYPE TIMESTAMP 
                    USING (CURRENT_DATE + end_time);
                END IF;
            END $$;
        """)

        conn.commit()
        print("All tables created successfully")

    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    reset_database() 