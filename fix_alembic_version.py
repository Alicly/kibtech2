from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Check if alembic_version table exists
        result = db.session.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'alembic_version'
            )
        """))
        table_exists = result.scalar()
        
        if not table_exists:
            # Create alembic_version table
            db.session.execute(text("""
                CREATE TABLE alembic_version (
                    version_num VARCHAR(32) NOT NULL
                )
            """))
            print("Created alembic_version table")
        
        # Update version number
        db.session.execute(text("""
            DELETE FROM alembic_version
        """))
        db.session.execute(text("""
            INSERT INTO alembic_version (version_num) 
            VALUES ('a798b54fecc1')
        """))
        
        db.session.commit()
        print("Successfully updated alembic_version table")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}") 