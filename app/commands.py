import click
from flask.cli import with_appcontext
from app import db
from app.models import User, Course, Student
from flask_login import current_user

@click.command('create-admin')
@with_appcontext
def create_admin():
    """Create an admin user."""
    username = click.prompt('Enter admin username', default='admin')
    email = click.prompt('Enter admin email', default='admin@kitelakpelttc.edu')
    password = click.prompt('Enter admin password', hide_input=True)
    
    # Check if admin already exists
    admin = User.query.filter_by(username=username).first()
    if admin:
        click.echo('Admin user already exists.')
        return
    
    # Create new admin user
    admin = User(
        username=username,
        email=email,
        role='admin',
        first_name='Admin',
        last_name='User'
    )
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    click.echo('Admin user created successfully.')

@click.command('create-test-users')
@with_appcontext
def create_test_users():
    """Create test users for all roles."""
    try:
        # Create admin user
        admin = User(
            username='admin',
            email='admin@kitelakpel.edu',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Create lecturer user
        lecturer = User(
            username='lecturer',
            email='lecturer@kitelakpel.edu',
            role='lecturer'
        )
        lecturer.set_password('lecturer123')
        db.session.add(lecturer)

        # Create student user
        student = User(
            username='student',
            email='student@kitelakpel.edu',
            role='student'
        )
        student.set_password('student123')
        db.session.add(student)

        db.session.commit()
        click.echo('Test users created successfully!')
        click.echo('\nLogin credentials:')
        click.echo('----------------')
        click.echo('Admin:')
        click.echo('  Username: admin')
        click.echo('  Password: admin123')
        click.echo('\nLecturer:')
        click.echo('  Username: lecturer')
        click.echo('  Password: lecturer123')
        click.echo('\nStudent:')
        click.echo('  Username: student')
        click.echo('  Password: student123')
    except Exception as e:
        click.echo(f'Error creating test users: {str(e)}')
        db.session.rollback()

@click.command('create-student-record')
@click.argument('username')
@with_appcontext
def create_student_record(username):
    """Create a Student record for an existing user."""
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(f'User {username} not found.')
        return
    
    if user.role != 'student':
        click.echo(f'User {username} is not a student.')
        return
    
    # Check if student record already exists
    if Student.query.filter_by(email=user.email).first():
        click.echo(f'Student record already exists for {username}.')
        return
    
    # Create student record
    student = Student(
        student_number=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        status='active'
    )
    
    try:
        db.session.add(student)
        db.session.commit()
        click.echo(f'Successfully created student record for {username}.')
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error creating student record: {str(e)}')

def init_app(app):
    app.cli.add_command(create_admin)
    app.cli.add_command(create_test_users)
    app.cli.add_command(create_student_record) 