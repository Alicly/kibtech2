from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_file, make_response
from flask_login import login_required, current_user
from app import db
from app.models import User, Course, ClassRoom, News, Event, Notification, LeadershipTeam, Student, SlideshowSlide, FeeStructure
from app.forms.admin import CourseForm, ClassRoomForm, NewsForm, EventForm, UserForm, MaintenanceModeForm, HomepageSettingsForm, UnitForm, SlideshowSlideForm, SlideshowSlideEditForm
from werkzeug.utils import secure_filename
import os
from datetime import datetime, time
from functools import wraps
from app.models.system_setting import SystemSetting
import csv
from io import BytesIO, StringIO
from xhtml2pdf import pisa
from sqlalchemy import text
from app.models.unit import Unit

bp = Blueprint('admin', __name__)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_students = User.query.filter_by(role='student').count()
    total_lecturers = User.query.filter_by(role='lecturer').count()
    total_courses = Course.query.count()
    total_classes = ClassRoom.query.count()
    recent_news = News.query.order_by(News.date.desc()).limit(5).all()
    upcoming_events = Event.query.filter(Event.date >= datetime.now()).order_by(Event.date).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_students=total_students,
                         total_lecturers=total_lecturers,
                         total_courses=total_courses,
                         total_classes=total_classes,
                         recent_news=recent_news,
                         upcoming_events=upcoming_events)

# User Management
@bp.route('/users')
@login_required
@admin_required
def users():
    # Get filter parameters from query string
    username = request.args.get('username', '').strip()
    email = request.args.get('email', '').strip()
    role = request.args.get('role', '').strip()
    registration_number = request.args.get('registration_number', '').strip()
    staff_id = request.args.get('staff_id', '').strip()
    lecturer_id = request.args.get('lecturer_id', '').strip()

    # Start with all users
    query = User.query
    if username:
        query = query.filter(User.username.ilike(f"%{username}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if role:
        query = query.filter(User.role == role)
    if registration_number:
        query = query.filter(User.registration_number.ilike(f"%{registration_number}%"))
    if staff_id:
        query = query.filter(User.staff_id.ilike(f"%{staff_id}%"))
    if lecturer_id:
        query = query.filter(User.lecturer_id.ilike(f"%{lecturer_id}%"))
    users = query.all()
    return render_template('admin/users.html', users=users, 
                           filter_username=username, filter_email=email, filter_role=role, 
                           filter_registration_number=registration_number, filter_staff_id=staff_id, filter_lecturer_id=lecturer_id)

@bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        try:
            # Check if email already exists
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email address already registered. Please use a different email.', 'danger')
                return redirect(url_for('admin.add_user'))
            # Check if username already exists
            existing_username = User.query.filter_by(username=form.username.data).first()
            if existing_username:
                flash('Username already taken. Please choose a different username.', 'danger')
                return redirect(url_for('admin.add_user'))
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
            # Set role-specific fields
            if form.role.data == 'student':
                user.registration_number = form.registration_number.data
                user.course_id = form.course_id.data
                user.department = form.department.data
            elif form.role.data == 'lecturer':
                user.lecturer_id = form.lecturer_id.data
                user.department = form.department.data
                user.specialization = form.specialization.data
            elif form.role.data == 'staff':
                user.staff_id = form.staff_id.data
                user.position = form.position.data
            db.session.add(user)
            # If creating a student, also create student record
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
            db.session.commit()  # Commit first to get student.id
            # Now set enrolled_courses only if not already present
            if form.role.data == 'student':
                student = Student.query.filter_by(email=form.email.data).first()
                course = Course.query.get(form.course_id.data)
                if course and course not in student.enrolled_courses:
                    student.enrolled_courses.append(course)
                db.session.commit()
            else:
                flash('User has been added successfully.', 'success')
                return redirect(url_for('admin.users'))
            flash('User has been added successfully.', 'success')
            return redirect(url_for('admin.users'))
        except Exception as e:
            from sqlalchemy.exc import IntegrityError
            if isinstance(e, IntegrityError):
                db.session.rollback()
                # Check if the user was actually created despite the integrity error
                user = User.query.filter_by(email=form.email.data).first()
                if user:
                    flash('User has been added successfully.', 'success')
                else:
                    flash('An error occurred while adding the user. Please try again.', 'danger')
                return redirect(url_for('admin.users'))
            else:
                db.session.rollback()
                flash(f'An unexpected error occurred: {str(e)}', 'danger')
                return redirect(url_for('admin.users'))
    return render_template('admin/user_form.html', form=form, title='Add User')

@bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        user.address = form.address.data
        user.role = form.role.data
        
        if form.password.data:
            user.set_password(form.password.data)
            
        # Clear previous role-specific fields
        user.registration_number = None
        user.course_id = None
        user.department = None
        user.lecturer_id = None
        user.specialization = None
        user.staff_id = None
        user.position = None
            
        # Set new role-specific fields
        if form.role.data == 'student':
            user.registration_number = form.registration_number.data
            # We will manage course through the relationship, not a direct ID on user
            # user.course_id = form.course_id.data 
            user.department = form.department.data
            
            # Update enrolled_courses association
            student = Student.query.filter_by(email=user.email).first()
            if student:
                new_course = Course.query.get(form.course_id.data)
                # Remove all courses except the new one (enforce one course per student)
                for course in student.enrolled_courses.all():
                    if new_course is None or course.id != new_course.id:
                        student.enrolled_courses.remove(course)
                # Add the new course only if not already enrolled
                if new_course and not student.enrolled_courses.filter_by(id=new_course.id).first():
                    student.enrolled_courses.append(new_course)
            
        elif form.role.data == 'lecturer':
            user.lecturer_id = form.lecturer_id.data
            user.department = form.department.data
            user.specialization = form.specialization.data
        elif form.role.data == 'staff':
            user.staff_id = form.staff_id.data
            user.position = form.position.data
            
        db.session.commit()
        flash('User has been updated successfully.', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/user_form.html', form=form, title='Edit User', user=user)

@bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    # Delete related student record if it exists
    if hasattr(user, 'student') and user.student:
        db.session.delete(user.student)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted successfully.', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/users/pending')
@login_required
@admin_required
def pending_users():
    users = User.query.filter(User.role.in_(['staff', 'lecturer']), User.is_approved == False).all()
    return render_template('admin/pending_users.html', users=users)

@bp.route('/users/<int:id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_user(id):
    user = User.query.get_or_404(id)
    user.is_approved = True
    db.session.commit()
    flash(f'User {user.username} has been approved.', 'success')
    return redirect(url_for('admin.pending_users'))

@bp.route('/users/<int:id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} has been rejected and deleted.', 'info')
    return redirect(url_for('admin.pending_users'))

# Course Management
@bp.route('/courses')
@login_required
@admin_required
def courses():
    courses = Course.query.all()
    return render_template('admin/courses.html', courses=courses)

@bp.route('/courses/<int:course_id>/units')
@login_required
@admin_required
def view_course_units(course_id):
    course = Course.query.get_or_404(course_id)
    units = course.units.all()
    return render_template('admin/course_units.html', course=course, units=units)

@bp.route('/courses/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            code=form.code.data,
            name=form.name.data,
            description=form.description.data,
            duration=form.duration.data,
            level=form.level.data,
            category=form.category.data,
            capacity=form.capacity.data,
            fee=form.fee.data,
            entry_requirements=form.entry_requirements.data,
            exam_body=form.exam_body.data,
            lecturer_id=form.lecturer_id.data if form.lecturer_id.data != 0 else None,
            is_active=form.is_active.data
        )
        
        # Handle image upload
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            course.image_url = filename
        
        db.session.add(course)
        db.session.commit()

        # Create a default fee structure for the new course
        fee_structure = FeeStructure(
            course_id=course.id,
            academic_year=str(datetime.now().year),  # e.g., "2024"
            semester="Full Course",
            type="Tuition",
            amount=course.fee,
            due_date=datetime.now(),
            description=f"Total tuition fee for {course.name}"
        )
        db.session.add(fee_structure)
        db.session.commit()

        flash('Course has been added successfully.', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/course_form.html', form=form, title='Add Course')

@bp.route('/courses/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_course(id):
    course = Course.query.get_or_404(id)
    form = CourseForm(obj=course)
    
    if form.validate_on_submit():
        course.code = form.code.data
        course.name = form.name.data
        course.description = form.description.data
        course.duration = form.duration.data
        course.level = form.level.data
        course.category = form.category.data
        course.capacity = form.capacity.data
        course.fee = form.fee.data
        course.entry_requirements = form.entry_requirements.data
        course.exam_body = form.exam_body.data
        course.lecturer_id = form.lecturer_id.data if form.lecturer_id.data != 0 else None
        course.is_active = form.is_active.data
        
        # Handle image upload
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            course.image_url = filename
        
        # Find and update all corresponding fee structures of type 'Tuition'
        fee_structures = FeeStructure.query.filter_by(course_id=course.id, type="Tuition").all()
        if fee_structures:
            for fee_structure in fee_structures:
                fee_structure.amount = course.fee
                fee_structure.updated_at = datetime.utcnow()
        else:
            # If no fee structure exists, create one
            fee_structure = FeeStructure(
                course_id=course.id,
                academic_year=str(datetime.now().year),
                semester="Full Course",
                type="Tuition",
                amount=course.fee,
                due_date=datetime.now(),
                description=f"Total tuition fee for {course.name}"
            )
            db.session.add(fee_structure)

        db.session.commit()
        flash('Course has been updated successfully.', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/course_form.html', form=form, title='Edit Course', course=course)

@bp.route('/courses/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash('Course has been deleted successfully.', 'success')
    return redirect(url_for('admin.courses'))

@bp.route('/create-default-course')
@login_required
@admin_required
def create_default_course():
    # Check if default course already exists
    default_course = Course.query.filter_by(code='CIT').first()
    if not default_course:
        default_course = Course(
            code='CIT',
            name='Certificate in Information Technology',
            description='A comprehensive course covering the fundamentals of Information Technology',
            duration='2 years',
            level='Certificate'
        )
        db.session.add(default_course)
        db.session.commit()
        flash('Default course created successfully.', 'success')
    else:
        flash('Default course already exists.', 'info')
    return redirect(url_for('admin.courses'))

# Class Management
@bp.route('/classes')
@login_required
@admin_required
def classes():
    classes = ClassRoom.query.all()
    return render_template('admin/classes.html', classes=classes)

@bp.route('/classes/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_class():
    form = ClassRoomForm()
    if form.validate_on_submit():
        # Convert time strings to datetime objects
        start_time_str = form.start_time.data
        end_time_str = form.end_time.data
        
        # Create datetime objects for today with the specified times
        today = datetime.now().date()
        start_time = datetime.combine(today, time.fromisoformat(start_time_str))
        end_time = datetime.combine(today, time.fromisoformat(end_time_str))
        
        class_room = ClassRoom(
            name=form.name.data,
            course_id=form.course_id.data,
            lecturer_id=form.lecturer_id.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            day=form.day.data,
            start_time=start_time,
            end_time=end_time,
            capacity=form.capacity.data
        )
        db.session.add(class_room)
        db.session.commit()
        flash('Class has been added successfully.', 'success')
        return redirect(url_for('admin.classes'))
    return render_template('admin/class_form.html', form=form, title='Add Class')

@bp.route('/classes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_class(id):
    class_room = ClassRoom.query.get_or_404(id)
    form = ClassRoomForm(obj=class_room)
    
    # Populate time fields with existing data
    if request.method == 'GET':
        if class_room.start_time:
            form.start_time.data = class_room.start_time.strftime('%H:%M')
        if class_room.end_time:
            form.end_time.data = class_room.end_time.strftime('%H:%M')
    
    if form.validate_on_submit():
        # Convert time strings to datetime objects
        start_time_str = form.start_time.data
        end_time_str = form.end_time.data
        
        # Create datetime objects for today with the specified times
        today = datetime.now().date()
        start_time = datetime.combine(today, time.fromisoformat(start_time_str))
        end_time = datetime.combine(today, time.fromisoformat(end_time_str))
        
        class_room.name = form.name.data
        class_room.course_id = form.course_id.data
        class_room.lecturer_id = form.lecturer_id.data
        class_room.description = form.description.data
        class_room.start_date = form.start_date.data
        class_room.end_date = form.end_date.data
        class_room.day = form.day.data
        class_room.start_time = start_time
        class_room.end_time = end_time
        class_room.capacity = form.capacity.data
        db.session.commit()
        flash('Class has been updated successfully.', 'success')
        return redirect(url_for('admin.classes'))
    return render_template('admin/class_form.html', form=form, title='Edit Class')

@bp.route('/classes/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_class(id):
    class_room = ClassRoom.query.get_or_404(id)
    db.session.delete(class_room)
    db.session.commit()
    flash('Class has been deleted successfully.', 'success')
    return redirect(url_for('admin.classes'))

# News Management
@bp.route('/news')
@login_required
@admin_required
def news():
    news_list = News.query.order_by(News.date.desc()).all()
    return render_template('admin/news.html', news_list=news_list)

@bp.route('/news/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = News(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            author=current_user.username
        )
        db.session.add(news)
        db.session.commit()
        
        # Create notification for all users
        notification = Notification(
            title='New News Posted',
            message=f'New news article: {news.title}',
            type='news',
            related_id=news.id
        )
        db.session.add(notification)
        db.session.commit()
        
        flash('News has been added successfully.', 'success')
        return redirect(url_for('admin.news'))
    return render_template('admin/news_form.html', form=form, title='Add News')

@bp.route('/news/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_news(id):
    news = News.query.get_or_404(id)
    form = NewsForm(obj=news)
    if form.validate_on_submit():
        news.title = form.title.data
        news.content = form.content.data
        news.category = form.category.data
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            news.image_url = filename
        db.session.commit()
        flash('News has been updated successfully.', 'success')
        return redirect(url_for('admin.news'))
    return render_template('admin/news_form.html', form=form, title='Edit News')

@bp.route('/news/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_news(id):
    news = News.query.get_or_404(id)
    db.session.delete(news)
    db.session.commit()
    flash('News has been deleted successfully.', 'success')
    return redirect(url_for('admin.news'))

# Event Management
@bp.route('/events')
@login_required
@admin_required
def events():
    events = Event.query.order_by(Event.date).all()
    return render_template('admin/events.html', events=events)

@bp.route('/events/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        # Extract date and time from event_date
        event_datetime = form.event_date.data
        event_date = event_datetime.date()
        event_time = event_datetime.time()
        
        # Create datetime objects for the database
        from datetime import datetime
        date_obj = datetime.combine(event_date, datetime.min.time())
        time_obj = datetime.combine(event_date, event_time)
        
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=date_obj,
            time=time_obj,
            location=form.location.data
        )
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            event.image_url = filename
            
        db.session.add(event)
        db.session.commit()
        
        # Create notification for all users
        notification = Notification(
            title='New Event Added',
            message=f'New event: {event.title} on {event.date.strftime("%Y-%m-%d")}',
            type='event',
            related_id=event.id
        )
        db.session.add(notification)
        db.session.commit()
        
        flash('Event has been added successfully.', 'success')
        return redirect(url_for('admin.events'))
    return render_template('admin/event_form.html', form=form, title='Add Event')

@bp.route('/events/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        # Extract date and time from event_date
        event_datetime = form.event_date.data
        event_date = event_datetime.date()
        event_time = event_datetime.time()
        
        # Create datetime objects for the database
        from datetime import datetime
        date_obj = datetime.combine(event_date, datetime.min.time())
        time_obj = datetime.combine(event_date, event_time)
        
        event.title = form.title.data
        event.description = form.description.data
        event.date = date_obj
        event.time = time_obj
        event.location = form.location.data
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            event.image_url = filename
        db.session.commit()
        flash('Event has been updated successfully.', 'success')
        return redirect(url_for('admin.events'))
    return render_template('admin/event_form.html', form=form, title='Edit Event')

@bp.route('/events/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event has been deleted successfully.', 'success')
    return redirect(url_for('admin.events'))

@bp.route('/leadership')
@login_required
@admin_required
def leadership():
    leaders = LeadershipTeam.query.order_by(LeadershipTeam.order).all()
    return render_template('admin/leadership.html', leaders=leaders)

@bp.route('/leadership/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_leader():
    if request.method == 'POST':
        leader = LeadershipTeam(
            name=request.form.get('name'),
            title=request.form.get('title'),
            position=request.form.get('position'),
            bio=request.form.get('bio'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            order=request.form.get('order', type=int),
            is_active=bool(request.form.get('is_active'))
        )
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                leader.image_url = filename
        
        db.session.add(leader)
        db.session.commit()
        flash('Leadership team member added successfully!', 'success')
        return redirect(url_for('admin.leadership'))
    
    return render_template('admin/add_leader.html')

@bp.route('/leadership/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_leader(id):
    leader = LeadershipTeam.query.get_or_404(id)
    
    if request.method == 'POST':
        leader.name = request.form.get('name')
        leader.title = request.form.get('title')
        leader.position = request.form.get('position')
        leader.bio = request.form.get('bio')
        leader.email = request.form.get('email')
        leader.phone = request.form.get('phone')
        leader.order = request.form.get('order', type=int)
        leader.is_active = bool(request.form.get('is_active'))
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                leader.image_url = filename
        
        db.session.commit()
        flash('Leadership team member updated successfully!', 'success')
        return redirect(url_for('admin.leadership'))
    
    return render_template('admin/edit_leader.html', leader=leader)

@bp.route('/leadership/delete/<int:id>')
@login_required
@admin_required
def delete_leader(id):
    leader = LeadershipTeam.query.get_or_404(id)
    db.session.delete(leader)
    db.session.commit()
    flash('Leadership team member deleted successfully!', 'success')
    return redirect(url_for('admin.leadership'))

@bp.route('/maintenance', methods=['GET', 'POST'])
@login_required
@admin_required
def maintenance():
    form = MaintenanceModeForm()
    current_mode = SystemSetting.get('maintenance_mode', 'off')
    if form.validate_on_submit():
        SystemSetting.set('maintenance_mode', form.maintenance_mode.data)
        flash(f"Maintenance mode set to: {form.maintenance_mode.data.upper()}", 'success')
        return redirect(url_for('admin.maintenance'))
    form.maintenance_mode.data = current_mode
    return render_template('admin/maintenance.html', form=form, current_mode=current_mode)

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        for key in ['registration_students', 'registration_staff', 'registration_lecturer', 'registration_admin', 'maintenance_mode']:
            value = request.form.get(key, 'disabled' if 'registration' in key else 'off')
            SystemSetting.set_setting(key, value)
        flash('Settings updated!', 'success')
        return redirect(url_for('admin.settings'))
    settings = {s.setting_key: s.setting_value for s in SystemSetting.query.all()}
    return render_template('admin/settings.html', settings=settings)

@bp.route('/export-users', methods=['GET'])
@login_required
@admin_required
def export_users():
    roles = ['student', 'lecturer', 'staff', 'admin']
    courses = Course.query.order_by(Course.name).all()
    return render_template('admin/export_users.html', roles=roles, courses=courses)

@bp.route('/export-users-pdf')
@login_required
@admin_required
def export_users_pdf():
    role = request.args.get('role')
    course_id = request.args.get('course_id')
    tvet_name = SystemSetting.query.get('tvet_name').value if SystemSetting.query.get('tvet_name') else 'KITELAKAPEL TECHNICAL TRAINING INSTITUTE'
    users = User.query.filter_by(role=role)
    course = None
    if role == 'student' and course_id:
        users = users.join(Student, Student.email == User.email).filter(Student.course_id == course_id)
        course = Course.query.get(course_id)
    users = users.all()
    list_type = f"List of {role.capitalize()}s"
    if role == 'student' and course:
        list_type = f"List of Students in {course.name} ({course.code})"
    date_generated = datetime.now().strftime('%Y-%m-%d %H:%M')
    html = render_template('admin/export_users_pdf.html', users=users, role=role, course=course, tvet_name=tvet_name, list_type=list_type, date_generated=date_generated)
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=pdf)
    pdf.seek(0)
    return send_file(pdf, mimetype='application/pdf', as_attachment=True, download_name='user_list.pdf')

@bp.route('/export-users-csv')
@login_required
@admin_required
def export_users_csv():
    role = request.args.get('role')
    course_id = request.args.get('course_id')
    users = User.query.filter_by(role=role)
    course = None
    if role == 'student' and course_id:
        users = users.join(Student, Student.email == User.email).filter(Student.course_id == course_id)
        course = Course.query.get(course_id)
    users = users.all()
    si = StringIO()
    writer = csv.writer(si)
    # Write header
    header = ['Username', 'First Name', 'Last Name', 'Email', 'Role', 'Phone']
    if role == 'student':
        header += ['Registration Number', 'Course']
    writer.writerow(header)
    for user in users:
        row = [user.username, user.first_name, user.last_name, user.email, user.role, user.phone]
        if role == 'student':
            student = Student.query.filter_by(email=user.email).first()
            row += [student.student_number if student else '', course.name if course else '']
        writer.writerow(row)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=user_list.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@bp.app_context_processor
def inject_pending_approvals():
    from app.models import User
    count = User.query.filter(User.role.in_(['staff', 'lecturer']), User.is_approved == False).count()
    return dict(pending_approvals_count=count) 

@bp.route('/homepage-settings', methods=['GET', 'POST'])
@login_required
@admin_required
def homepage_settings():
    form = HomepageSettingsForm()
    
    if form.validate_on_submit():
        # Handle file uploads
        if form.institute_logo.data:
            filename = secure_filename(form.institute_logo.data.filename)
            form.institute_logo.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            SystemSetting.set_setting('institute_logo', filename, 'image', 'Institute logo image')
        
        if form.hero_background.data:
            filename = secure_filename(form.hero_background.data.filename)
            form.hero_background.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            SystemSetting.set_setting('hero_background', filename, 'image', 'Hero section background image')
        
        if form.campus_image.data:
            filename = secure_filename(form.campus_image.data.filename)
            form.campus_image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            SystemSetting.set_setting('campus_image', filename, 'image', 'Campus image for homepage')
        
        if form.about_image.data:
            filename = secure_filename(form.about_image.data.filename)
            form.about_image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            SystemSetting.set_setting('about_image', filename, 'image', 'About section image')
        
        # Save text settings
        SystemSetting.set_setting('hero_title', form.hero_title.data, 'text', 'Hero section title')
        SystemSetting.set_setting('hero_subtitle', form.hero_subtitle.data, 'text', 'Hero section subtitle')
        SystemSetting.set_setting('institute_name', form.institute_name.data, 'text', 'Institute name')
        SystemSetting.set_setting('institute_tagline', form.institute_tagline.data, 'text', 'Institute tagline')
        SystemSetting.set_setting('contact_email', form.contact_email.data, 'text', 'Contact email')
        SystemSetting.set_setting('contact_phone', form.contact_phone.data, 'text', 'Contact phone')
        SystemSetting.set_setting('contact_address', form.contact_address.data, 'text', 'Contact address')
        
        flash('Homepage settings updated successfully!', 'success')
        return redirect(url_for('admin.homepage_settings'))
    
    # Populate form with current settings
    form.hero_title.data = SystemSetting.get_setting('hero_title', 'Empowering Kenya\'s Future Through Technical Education')
    form.hero_subtitle.data = SystemSetting.get_setting('hero_subtitle', 'Building a skilled workforce for Kenya\'s development through quality technical and vocational education at KITELAKAPEL TECHNICAL TRAINING INSTITUTE.')
    form.institute_name.data = SystemSetting.get_setting('institute_name', 'KITELAKAPEL TECHNICAL TRAINING INSTITUTE')
    form.institute_tagline.data = SystemSetting.get_setting('institute_tagline', 'Empowering Through Technical Education')
    form.contact_email.data = SystemSetting.get_setting('contact_email', 'info@kitelakapel.ac.ke')
    form.contact_phone.data = SystemSetting.get_setting('contact_phone', '+254 700 000 000')
    form.contact_address.data = SystemSetting.get_setting('contact_address', 'Kitelakapel, Kenya')
    
    # Get current images
    current_logo = SystemSetting.get_setting('institute_logo')
    current_hero_bg = SystemSetting.get_setting('hero_background')
    current_campus = SystemSetting.get_setting('campus_image')
    current_about = SystemSetting.get_setting('about_image')
    
    return render_template('admin/homepage_settings.html', 
                         form=form, 
                         current_logo=current_logo,
                         current_hero_bg=current_hero_bg,
                         current_campus=current_campus,
                         current_about=current_about)

@bp.route('/courses/<int:course_id>/units/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_unit(course_id):
    course = Course.query.get_or_404(course_id)
    form = UnitForm(course_id=course_id)
    if form.validate_on_submit():
        unit = Unit(
            code=form.code.data,
            name=form.name.data,
            description=form.description.data,
            credits=form.credits.data,
            course_id=course_id
        )
        db.session.add(unit)
        db.session.commit()
        flash('Unit added successfully.', 'success')
        return redirect(url_for('admin.view_course_units', course_id=course_id))
    return render_template('admin/unit_form.html', form=form, title='Add Unit', course=course)

@bp.route('/units/<int:unit_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_unit(unit_id):
    unit = Unit.query.get_or_404(unit_id)
    form = UnitForm(obj=unit, course_id=unit.course_id)
    if form.validate_on_submit():
        unit.code = form.code.data
        unit.name = form.name.data
        unit.description = form.description.data
        unit.credits = form.credits.data
        db.session.commit()
        flash('Unit updated successfully.', 'success')
        return redirect(url_for('admin.view_course_units', course_id=unit.course_id))
    return render_template('admin/unit_form.html', form=form, title='Edit Unit', course=unit.course)

@bp.route('/units/<int:unit_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_unit(unit_id):
    unit = Unit.query.get_or_404(unit_id)
    course_id = unit.course_id
    db.session.delete(unit)
    db.session.commit()
    flash('Unit has been deleted successfully.', 'success')
    return redirect(url_for('admin.view_course_units', course_id=course_id))

# Slideshow Management
@bp.route('/slideshow')
@login_required
@admin_required
def slideshow():
    slides = SlideshowSlide.query.order_by(SlideshowSlide.order.asc()).all()
    return render_template('admin/slideshow.html', slides=slides)

@bp.route('/slideshow/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_slideshow_slide():
    form = SlideshowSlideForm()
    if form.validate_on_submit():
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            
            slide = SlideshowSlide(
                title=form.title.data,
                description=form.description.data,
                image_url=filename,
                order=form.order.data or 0,
                is_active=form.is_active.data
            )
            db.session.add(slide)
            db.session.commit()
            flash('Slideshow slide has been added successfully.', 'success')
            return redirect(url_for('admin.slideshow'))
    return render_template('admin/slideshow_form.html', form=form, title='Add Slideshow Slide')

@bp.route('/slideshow/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_slideshow_slide(id):
    slide = SlideshowSlide.query.get_or_404(id)
    form = SlideshowSlideEditForm(obj=slide)
    if form.validate_on_submit():
        slide.title = form.title.data
        slide.description = form.description.data
        slide.order = form.order.data or 0
        slide.is_active = form.is_active.data
        
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            slide.image_url = filename
            
        db.session.commit()
        flash('Slideshow slide has been updated successfully.', 'success')
        return redirect(url_for('admin.slideshow'))
    return render_template('admin/slideshow_form.html', form=form, title='Edit Slideshow Slide')

@bp.route('/slideshow/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_slideshow_slide(id):
    slide = SlideshowSlide.query.get_or_404(id)
    db.session.delete(slide)
    db.session.commit()
    flash('Slideshow slide has been deleted successfully.', 'success')
    return redirect(url_for('admin.slideshow'))

@bp.route('/slideshow/reorder', methods=['POST'])
@login_required
@admin_required
def reorder_slideshow():
    slide_orders = request.json.get('slide_orders', [])
    for slide_data in slide_orders:
        slide = SlideshowSlide.query.get(slide_data['id'])
        if slide:
            slide.order = slide_data['order']
    db.session.commit()
    return {'success': True} 