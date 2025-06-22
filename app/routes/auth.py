from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import db
from app.models import User, Student, Course
from app.forms.auth import LoginForm, RegistrationForm, ChangePasswordForm, UserSettingsForm
from werkzeug.urls import url_parse
from app.models.system_setting import SystemSetting

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        # Check approval for staff/lecturer
        if user.role in ['staff', 'lecturer'] and not user.is_approved:
            flash('Your account is pending admin approval. Please wait for approval.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Check if user's role matches the selected role
        if form.role.data and user.role != form.role.data:
            flash(f'This account is not registered as a {form.role.data}. Please select the correct role.', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            # Redirect to role-specific dashboard
            if user.role == 'admin':
                next_page = url_for('admin.dashboard')
            elif user.role == 'lecturer':
                next_page = url_for('lecturer.dashboard')
            elif user.role == 'staff':
                next_page = url_for('staff.dashboard')
            elif user.role == 'student':
                next_page = url_for('student.dashboard')
            else:
                flash('Invalid user role', 'error')
                return redirect(url_for('auth.login'))
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Enforce registration settings
        setting_key = f"registration_{form.role.data}"
        setting = SystemSetting.query.get(setting_key)
        if not setting or setting.value != 'enabled':
            flash(f'Registration for {form.role.data.capitalize()}s is currently disabled. Please contact the administrator.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Check if email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email address already registered. Please use a different email or login.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Check if username already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken. Please choose a different username.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create user record
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            address=form.address.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        # Set approval status
        if form.role.data in ['staff', 'lecturer']:
            user.is_approved = False
        else:
            user.is_approved = True
        
        # Set role-specific fields
        if form.role.data == 'lecturer':
            user.lecturer_id = form.lecturer_id.data
            user.department = form.department.data
            user.specialization = form.specialization.data
        elif form.role.data == 'staff':
            user.staff_id = form.staff_id.data
            user.position = form.position.data
        
        db.session.add(user)
        
        # If registering as a student, create student record
        if form.role.data == 'student':
            student = Student(
                student_number=form.registration_number.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone=form.phone.data,
                address=form.address.data,
                date_of_birth=form.date_of_birth.data,
                gender=form.gender.data,
                course_id=form.course_id.data,
                status='active'
            )
            db.session.add(student)
            # Add to enrolled_courses association
            course = Course.query.get(form.course_id.data)
            if course:
                student.enrolled_courses.append(course)
        
        # If registering as a lecturer, add selected courses
        if form.role.data == 'lecturer' and form.lecturer_courses.data:
            for course_id in form.lecturer_courses.data:
                course = Course.query.get(course_id)
                if course:
                    user.courses_teaching.append(course)
        
        try:
            db.session.commit()
            flash('Congratulations, you are now a registered user!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/fetch_student_data/<reg_number>')
def fetch_student_data(reg_number):
    """API endpoint to fetch student data by registration number"""
    try:
        student = Student.query.filter_by(student_number=reg_number).first()
        if student:
            return jsonify({
                'success': True,
                'student': {
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'email': student.email,
                    'phone': student.phone,
                    'address': student.address,
                    'date_of_birth': student.date_of_birth.isoformat() if student.date_of_birth else None,
                    'gender': student.gender,
                    'course_id': student.course_id
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', title='Profile')

@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('auth.profile'))
        flash('Invalid old password.', 'danger')
    return render_template('auth/change_password.html', form=form)

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UserSettingsForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your settings have been updated.', 'success')
        return redirect(url_for('auth.settings'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('auth/settings.html', title='Settings', form=form) 