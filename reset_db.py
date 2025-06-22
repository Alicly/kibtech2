from app import create_app, db

def reset_database():
    app = create_app()
    
    with app.app_context():
        print("Dropping all existing tables...")
        db.drop_all()
        
        print("Creating all tables...")
        db.create_all()
        
        print("Database reset completed! Run 'python init_db.py' to add sample data.")

if __name__ == '__main__':
    reset_database() 