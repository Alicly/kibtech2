import click
from flask.cli import with_appcontext
from app import db
from app.models import User, Student
from flask_login import current_user

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

@click.command('create-student-for-current-user')
@with_appcontext
def create_student_for_current_user():
    """Create a Student record for the currently logged in user."""
    if not current_user.is_authenticated:
        click.echo('No user is currently logged in.')
        return
    
    if current_user.role != 'student':
        click.echo(f'Current user is not a student (role: {current_user.role}).')
        return
    
    # Check if student record already exists
    if Student.query.filter_by(email=current_user.email).first():
        click.echo(f'Student record already exists for {current_user.username}.')
        return
    
    # Create student record
    student = Student(
        student_number=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        status='active'
    )
    
    try:
        db.session.add(student)
        db.session.commit()
        click.echo(f'Successfully created student record for {current_user.username}.')
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error creating student record: {str(e)}')

def init_app(app):
    app.cli.add_command(create_student_record)
    app.cli.add_command(create_student_for_current_user) 