from app import create_app, db
from app.models.unit import Unit
from sqlalchemy import text

def backup_units():
    return [
        {
            'code': u.code,
            'name': u.name,
            'description': u.description,
            'credits': u.credits,
            'course_id': u.course_id,
            'created_at': u.created_at,
            'updated_at': u.updated_at,
        }
        for u in Unit.query.all()
    ]

def drop_and_recreate_units_table():
    db.session.execute(text('DROP TABLE IF EXISTS units'))
    db.session.commit()
    db.session.execute(text('''
        CREATE TABLE units (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR(20) NOT NULL,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            credits INTEGER,
            created_at DATETIME,
            updated_at DATETIME,
            course_id INTEGER NOT NULL,
            FOREIGN KEY(course_id) REFERENCES courses(id),
            UNIQUE(code, course_id)
        )
    '''))
    db.session.commit()

def restore_units(units):
    for u in units:
        db.session.execute(text('''
            INSERT INTO units (code, name, description, credits, created_at, updated_at, course_id)
            VALUES (:code, :name, :description, :credits, :created_at, :updated_at, :course_id)
        '''), u)
    db.session.commit()

def main():
    app = create_app()
    with app.app_context():
        print('Backing up existing units...')
        units = backup_units()
        print(f'Backed up {len(units)} units.')
        print('Dropping and recreating units table...')
        drop_and_recreate_units_table()
        print('Restoring units...')
        restore_units(units)
        print('Done.')

if __name__ == '__main__':
    main() 