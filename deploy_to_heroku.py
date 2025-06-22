#!/usr/bin/env python3
"""
Heroku Deployment Script for TVET Management System
This script helps set up and deploy the application to Heroku
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return None

def check_heroku_cli():
    """Check if Heroku CLI is installed"""
    print("🔍 Checking Heroku CLI installation...")
    try:
        subprocess.run(["heroku", "--version"], check=True, capture_output=True)
        print("✅ Heroku CLI is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Heroku CLI is not installed")
        print("Please install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli")
        return False

def create_heroku_app(app_name):
    """Create a new Heroku app"""
    if not app_name:
        app_name = input("Enter your Heroku app name (or press Enter for auto-generated name): ").strip()
    
    if app_name:
        command = f"heroku create {app_name}"
    else:
        command = "heroku create"
    
    result = run_command(command, "Creating Heroku app")
    if result:
        # Extract app URL from output
        lines = result.split('\n')
        for line in lines:
            if 'https://' in line and 'herokuapp.com' in line:
                return line.strip()
    return None

def setup_database():
    """Set up PostgreSQL database on Heroku"""
    print("\n🗄️ Setting up PostgreSQL database...")
    
    # Add PostgreSQL addon
    result = run_command("heroku addons:create heroku-postgresql:mini", "Adding PostgreSQL addon")
    if not result:
        print("⚠️ Failed to add PostgreSQL addon. You may need to add it manually.")
        return False
    
    # Get database URL
    result = run_command("heroku config:get DATABASE_URL", "Getting database URL")
    if result:
        print(f"✅ Database URL configured: {result.strip()}")
        return True
    return False

def set_environment_variables():
    """Set up environment variables"""
    print("\n🔧 Setting up environment variables...")
    
    # Set secret key
    secret_key = os.urandom(24).hex()
    run_command(f'heroku config:set SECRET_KEY="{secret_key}"', "Setting SECRET_KEY")
    
    # Set Flask environment
    run_command('heroku config:set FLASK_ENV=production', "Setting FLASK_ENV")
    
    # Set other variables if needed
    run_command('heroku config:set FLASK_APP=app.py', "Setting FLASK_APP")
    
    print("✅ Environment variables configured")

def deploy_application():
    """Deploy the application to Heroku"""
    print("\n🚀 Deploying application to Heroku...")
    
    # Initialize git if not already done
    if not os.path.exists('.git'):
        run_command("git init", "Initializing git repository")
        run_command("git add .", "Adding files to git")
        run_command('git commit -m "Initial commit for Heroku deployment"', "Making initial commit")
    
    # Add Heroku remote if not exists
    result = run_command("git remote -v", "Checking git remotes")
    if "heroku" not in result:
        run_command("heroku git:remote -a $(heroku apps:info --json | python -c 'import sys, json; print(json.load(sys.stdin)[\"app\"][\"name\"])')", "Adding Heroku remote")
    
    # Deploy to Heroku
    result = run_command("git push heroku main", "Deploying to Heroku")
    if not result:
        # Try master branch if main doesn't exist
        result = run_command("git push heroku master", "Deploying to Heroku (master branch)")
    
    return result is not None

def run_migrations():
    """Run database migrations"""
    print("\n📊 Running database migrations...")
    result = run_command("heroku run flask db upgrade", "Running database migrations")
    return result is not None

def create_admin_user():
    """Create an admin user"""
    print("\n👤 Creating admin user...")
    
    # Create a script to add admin user
    admin_script = '''
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    # Check if admin exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@tvet.ac.ke',
            first_name='System',
            last_name='Administrator',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
    else:
        print("Admin user already exists!")
'''
    
    with open('create_admin.py', 'w') as f:
        f.write(admin_script)
    
    result = run_command("heroku run python create_admin.py", "Creating admin user")
    
    # Clean up
    if os.path.exists('create_admin.py'):
        os.remove('create_admin.py')
    
    return result is not None

def main():
    """Main deployment function"""
    print("🚀 TVET Management System - Heroku Deployment")
    print("=" * 50)
    
    # Check prerequisites
    if not check_heroku_cli():
        return
    
    # Get app name
    app_name = input("Enter your Heroku app name (or press Enter for auto-generated): ").strip()
    
    # Create app
    app_url = create_heroku_app(app_name)
    if not app_url:
        print("❌ Failed to create Heroku app")
        return
    
    print(f"✅ Heroku app created: {app_url}")
    
    # Setup database
    if not setup_database():
        print("⚠️ Database setup failed. You may need to set it up manually.")
    
    # Set environment variables
    set_environment_variables()
    
    # Deploy application
    if not deploy_application():
        print("❌ Deployment failed")
        return
    
    # Run migrations
    if not run_migrations():
        print("⚠️ Database migrations failed. You may need to run them manually.")
    
    # Create admin user
    if not create_admin_user():
        print("⚠️ Admin user creation failed. You may need to create it manually.")
    
    print("\n🎉 Deployment completed!")
    print(f"🌐 Your application is available at: {app_url}")
    print("\n📋 Next steps:")
    print("1. Visit your application URL")
    print("2. Login with admin/admin123")
    print("3. Change the admin password")
    print("4. Add your courses and users")
    print("\n🔧 Useful commands:")
    print("- View logs: heroku logs --tail")
    print("- Open app: heroku open")
    print("- Run shell: heroku run flask shell")
    print("- Run migrations: heroku run flask db upgrade")

if __name__ == "__main__":
    main() 