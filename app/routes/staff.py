from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models import Course, Module, Enrollment, TeachingMaterial, Student, Fee, Announcement, News, Event, Payment
from app import db
from sqlalchemy import or_
from datetime import datetime

bp = Blueprint('staff', __name__, url_prefix='/staff')

@bp.before_request
def before_request():
    if not current_user.is_authenticated or current_user.role != 'staff':
        flash('Access denied. Staff access required.', 'danger')
        return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get lecturer's courses
    courses = Course.query.filter_by(lecturer_id=current_user.id).all()
    
    # Get enrollments for these courses
    enrollments = Enrollment.query.join(Course).filter(Course.lecturer_id == current_user.id).all()
    
    return render_template('staff/dashboard.html',
                         courses=courses,
                         enrollments=enrollments)

@bp.route('/courses')
@login_required
def courses():
    courses = Course.query.filter_by(lecturer_id=current_user.id).all()
    return render_template('staff/courses.html', courses=courses)

@bp.route('/students')
@login_required
def students():
    # Get filter parameters
    first_name = request.args.get('first_name', '').strip()
    last_name = request.args.get('last_name', '').strip()
    email = request.args.get('email', '').strip()
    student_number = request.args.get('student_number', '').strip()
    course_id = request.args.get('course_id', '').strip()
    gender = request.args.get('gender', '').strip()
    status = request.args.get('status', '').strip()
    phone = request.args.get('phone', '').strip()

    query = Student.query
    if first_name:
        query = query.filter(Student.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Student.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Student.email.ilike(f"%{email}%"))
    if student_number:
        query = query.filter(Student.student_number.ilike(f"%{student_number}%"))
    if course_id and course_id.isdigit():
        query = query.filter(Student.course_id == int(course_id))
    if gender:
        query = query.filter(Student.gender == gender)
    if status:
        query = query.filter(Student.status == status)
    if phone:
        query = query.filter(Student.phone.ilike(f"%{phone}%"))
    students = query.all()
    from app.models import Course
    courses = Course.query.filter_by(is_active=True).order_by(Course.name).all()
    return render_template('staff/students.html', students=students, courses=courses,
        filter_first_name=first_name, filter_last_name=last_name, filter_email=email, filter_student_number=student_number,
        filter_course_id=course_id, filter_gender=gender, filter_status=status, filter_phone=phone)

@bp.route('/materials')
@login_required
def materials():
    materials = TeachingMaterial.query.filter_by(lecturer_id=current_user.id).all()
    return render_template('staff/materials.html', materials=materials)

@bp.route('/fees', methods=['GET', 'POST'])
@login_required
def fees():
    students = Student.query.all()
    # Fee updating logic
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        amount = request.form.get('amount')
        academic_year = request.form.get('academic_year')
        semester = request.form.get('semester')
        due_date_str = request.form.get('due_date')
        if student_id and amount and academic_year and semester and due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                fee = Fee(
                    student_id=student_id,
                    amount=amount,
                    academic_year=academic_year,
                    semester=semester,
                    due_date=due_date,
                    status='pending'
                )
                db.session.add(fee)
                db.session.commit()
                flash('Fee record added!', 'success')
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
        return redirect(url_for('staff.fees'))
    return render_template('staff/fees.html', students=students)

@bp.route('/fees/<int:student_id>/update', methods=['POST'])
@login_required
def update_student_fees(student_id):
    student = Student.query.get_or_404(student_id)
    
    fee_id = request.form.get('fee_id')
    action = request.form.get('action')  # 'add_payment', 'update_fee', 'add_note'
    notes = request.form.get('notes')
    
    if action == 'add_payment':
        amount = float(request.form.get('amount'))
        payment_method = request.form.get('payment_method')
        reference_number = request.form.get('reference_number')
        
        # Create payment record
        payment = Payment(
            student_id=student.id,
            fee_id=fee_id,
            amount=amount,
            payment_date=datetime.now(),
            payment_method=payment_method,
            reference_number=reference_number,
            status='completed',
            created_by=current_user.id,
            notes=notes
        )
        db.session.add(payment)
        
        # Update fee status
        fee = Fee.query.get(fee_id)
        if fee:
            fee.update_status()
            fee.updated_by = current_user.id
            if notes:
                fee.notes = notes
        
        flash('Payment recorded successfully!', 'success')
        
    elif action == 'update_fee':
        fee = Fee.query.get(fee_id)
        if fee:
            fee.amount = float(request.form.get('amount'))
            fee.due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d').date()
            fee.updated_by = current_user.id
            if notes:
                fee.notes = notes
            fee.update_status()
            flash('Fee updated successfully!', 'success')
    
    elif action == 'add_note':
        fee = Fee.query.get(fee_id)
        if fee:
            fee.notes = notes
            fee.updated_by = current_user.id
            flash('Note added successfully!', 'success')
    
    db.session.commit()
    return redirect(url_for('staff.student_profile', student_id=student.id))

@bp.route('/student/<int:student_id>')
@login_required
def student_profile(student_id):
    student = Student.query.get_or_404(student_id)
    fees = Fee.query.filter_by(student_id=student.id).all()
    # Analytics: total paid, total due
    total_paid = sum(f.amount for f in fees if f.status == 'paid')
    total_due = sum(f.amount for f in fees if f.status != 'paid')
    return render_template('staff/student_profile.html', student=student, fees=fees, total_paid=total_paid, total_due=total_due)

@bp.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    students = [enrollment.student for enrollment in course.enrollments]
    # Analytics: number of students, total fees due
    total_students = len(students)
    total_fees_due = sum(sum(f.amount for f in Fee.query.filter_by(student_id=s.id, status='pending')) for s in students)
    return render_template('staff/course_detail.html', course=course, students=students, total_students=total_students, total_fees_due=total_fees_due)

@bp.route('/students/search')
@login_required
def search_students():
    # Advanced search: redirect to /students with query params
    q = request.args.get('q', '').strip()
    return redirect(url_for('staff.students', first_name=q, last_name=q, email=q, student_number=q))

@bp.route('/courses/search')
@login_required
def search_courses():
    q = request.args.get('q', '')
    courses = Course.query.filter(Course.name.ilike(f'%{q}%')).all()
    return render_template('staff/courses.html', courses=courses, search_query=q)

@bp.route('/resources')
@login_required
def resources():
    # You can customize what resources staff should see
    return render_template('staff/resources.html')

@bp.route('/announcements', methods=['GET', 'POST'])
@login_required
def announcements():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            announcement = Announcement(
                title=title,
                content=content,
                created_by=current_user.id,
                created_at=db.func.now(),
                status='active',
                priority='normal'
            )
            db.session.add(announcement)
            db.session.commit()
            flash('Announcement posted!', 'success')
        else:
            flash('Title and content are required.', 'danger')
        return redirect(url_for('staff.announcements'))
    announcements = Announcement.query.filter_by(status='active').order_by(Announcement.created_at.desc()).all()
    return render_template('staff/announcements.html', announcements=announcements)

@bp.route('/announcements/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(id):
    announcement = Announcement.query.get_or_404(id)
    if announcement.created_by != current_user.id and current_user.role != 'admin':
        flash('You do not have permission to edit this announcement.', 'danger')
        return redirect(url_for('staff.announcements'))
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            announcement.title = title
            announcement.content = content
            db.session.commit()
            flash('Announcement updated!', 'success')
            return redirect(url_for('staff.announcements'))
        else:
            flash('Title and content are required.', 'danger')
    return render_template('staff/edit_announcement.html', announcement=announcement)

@bp.route('/announcements/delete/<int:id>', methods=['POST'])
@login_required
def delete_announcement(id):
    announcement = Announcement.query.get_or_404(id)
    if announcement.created_by != current_user.id and current_user.role != 'admin':
        flash('You do not have permission to delete this announcement.', 'danger')
        return redirect(url_for('staff.announcements'))
    db.session.delete(announcement)
    db.session.commit()
    flash('Announcement deleted.', 'info')
    return redirect(url_for('staff.announcements'))

@bp.route('/news', methods=['GET', 'POST'])
@login_required
def news():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            news_item = News(
                title=title,
                content=content,
                created_by=current_user.id,
                created_at=db.func.now(),
                status='active'
            )
            db.session.add(news_item)
            db.session.commit()
            flash('News posted!', 'success')
        else:
            flash('Title and content are required.', 'danger')
        return redirect(url_for('staff.news'))
    news_list = News.query.filter_by(status='active').order_by(News.created_at.desc()).all()
    return render_template('staff/news.html', news_list=news_list)

@bp.route('/news/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    news_item = News.query.get_or_404(id)
    if news_item.created_by != current_user.id and current_user.role != 'admin':
        flash('You do not have permission to edit this news.', 'danger')
        return redirect(url_for('staff.news'))
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            news_item.title = title
            news_item.content = content
            db.session.commit()
            flash('News updated!', 'success')
            return redirect(url_for('staff.news'))
        else:
            flash('Title and content are required.', 'danger')
    return render_template('staff/edit_news.html', news_item=news_item)

@bp.route('/news/delete/<int:id>', methods=['POST'])
@login_required
def delete_news(id):
    news_item = News.query.get_or_404(id)
    if news_item.created_by != current_user.id and current_user.role != 'admin':
        flash('You do not have permission to delete this news.', 'danger')
        return redirect(url_for('staff.news'))
    db.session.delete(news_item)
    db.session.commit()
    flash('News deleted.', 'info')
    return redirect(url_for('staff.news'))

@bp.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')
        if title and description and date and time and location:
            event = Event(
                title=title,
                description=description,
                date=date,
                time=time,
                location=location,
                created_at=db.func.now(),
                status='upcoming'
            )
            db.session.add(event)
            db.session.commit()
            flash('Event posted!', 'success')
        else:
            flash('All fields are required.', 'danger')
        return redirect(url_for('staff.events'))
    events_list = Event.query.order_by(Event.date.desc()).all()
    return render_template('staff/events.html', events_list=events_list)

@bp.route('/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    if event.created_by != current_user.id and current_user.role != 'admin':
        flash('You do not have permission to edit this event.', 'danger')
        return redirect(url_for('staff.events'))
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')
        if title and description and date and time and location:
            event.title = title
            event.description = description
            event.date = date
            event.time = time
            event.location = location
            db.session.commit()
            flash('Event updated!', 'success')
            return redirect(url_for('staff.events'))
        else:
            flash('All fields are required.', 'danger')
    return render_template('staff/edit_event.html', event=event)

@bp.route('/events/delete/<int:id>', methods=['POST'])
@login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    if event.created_by != current_user.id and current_user.role != 'admin':
        flash('You do not have permission to delete this event.', 'danger')
        return redirect(url_for('staff.events'))
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.', 'info')
    return redirect(url_for('staff.events')) 