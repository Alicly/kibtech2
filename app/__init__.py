import os
from flask import Flask, render_template, request
from config import Config
from app.extensions import db, migrate, login_manager
from app.models.system_setting import SystemSetting
from flask_login import current_user
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import student_course_enrollments
from sqlalchemy import text

def ensure_upload_folder_exists(app):
    """Ensure the upload folder exists and create it if it doesn't."""
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload folder exists
    ensure_upload_folder_exists(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.routes.lecturer import bp as lecturer_bp
    app.register_blueprint(lecturer_bp, url_prefix='/lecturer')
    
    from app.routes.student import student_bp
    app.register_blueprint(student_bp, url_prefix='/student')
    
    from app.routes.staff import bp as staff_bp
    app.register_blueprint(staff_bp, url_prefix='/staff')
    
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.routes.faq import bp as faq_bp
    app.register_blueprint(faq_bp, url_prefix='/faq')
    
    from app.routes.alumni import bp as alumni_bp
    app.register_blueprint(alumni_bp, url_prefix='/alumni')
    
    from app.routes.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/profile')
    
    # Import models to ensure they are registered with SQLAlchemy
    from app.models import user, student, course, enrollment, assignment, grade, attendance, news, event, notification, leadership, class_room, module, unit, fee, payment, exam, teaching_material, activity_log, unit_registration

    # Register CLI commands
    @app.cli.command('init-db')
    def init_db_command():
        """Initialize the database."""
        db.create_all()
        print('Database tables created successfully!')

    @app.cli.command('reset-db')
    def reset_db_command():
        """Reset the database."""
        db.drop_all()
        db.create_all()
        print('Database reset successfully!')

    @app.before_request
    def check_maintenance_mode():
        # Allow static files and admin settings page
        if request.endpoint and (request.endpoint.startswith('static') or request.endpoint == 'admin.settings'):
            return
        # Allow admin users to bypass maintenance mode
        if current_user.is_authenticated and getattr(current_user, 'role', None) == 'admin':
            return
        setting = SystemSetting.query.get('maintenance_mode')
        if setting and setting.value == 'on':
            return render_template('errors/maintenance.html'), 503

    with app.app_context():
        populate_student_course_enrollments()

    return app

def populate_student_course_enrollments():
    with db.engine.connect() as conn:
        students = Student.query.filter(Student.course_id.isnot(None)).all()
        for student in students:
            course_id = student.course_id
            # Check if already in association table
            exists = conn.execute(text('''
                SELECT 1 FROM student_course_enrollments WHERE student_id = :sid AND course_id = :cid
            '''), {'sid': student.id, 'cid': course_id}).fetchone()
            if not exists:
                conn.execute(text('''
                    INSERT INTO student_course_enrollments (student_id, course_id) VALUES (:sid, :cid)
                '''), {'sid': student.id, 'cid': course_id})
        conn.commit()

# Create the app instance
app = create_app()

# Note: All routes are now handled by blueprints, no need to import routes.py 