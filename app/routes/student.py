from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, current_app, jsonify, make_response
from flask_login import login_required, current_user
from app import db
from app.models import (
    User, Course, Unit, UnitRegistration, Grade,
    FeeStructure, Payment, Assignment, Attendance, ClassSchedule,
    AssignmentSubmission, Student, ClassRoom, Fee, Exam, ExamResult
)
import os
from datetime import datetime, timedelta
import tempfile
import csv
from io import StringIO, BytesIO
from app.models.activity_log import ActivityLog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io

try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    PDFKIT_AVAILABLE = False

student_bp = Blueprint('student', __name__)

@student_bp.before_request
def before_request():
    print("DEBUG: User authenticated:", current_user.is_authenticated)
    print("DEBUG: User role:", getattr(current_user, 'role', None))
    if not current_user.is_authenticated or current_user.role != 'student':
        flash('Access denied. Please log in as a student.', 'error')
        return redirect(url_for('auth.login'))

@student_bp.route('/dashboard')
@login_required
def dashboard():
    # Debug logging
    current_app.logger.debug(f"Current user: {current_user}")
    current_app.logger.debug(f"Current user ID: {current_user.id}")
    current_app.logger.debug(f"Current user role: {current_user.role}")
    
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    current_app.logger.debug(f"Found student record: {student}")
    
    if not student:
        current_app.logger.debug("No student record found, attempting to create one")
        try:
            # Get the first available course
            course = Course.query.first()
            if not course:
                flash('No courses available. Please contact the administrator.', 'error')
                return redirect(url_for('main.index'))
                
            student = Student(
                student_number=f"STU{current_user.id:04d}",
                first_name=current_user.first_name,
                last_name=current_user.last_name,
                email=current_user.email,
                course_id=course.id,
                status='active'
            )
            db.session.add(student)
            db.session.commit()
            current_app.logger.debug(f"Created new student record: {student}")
            flash('Student record created successfully.', 'success')
        except Exception as e:
            current_app.logger.error(f"Error creating student record: {str(e)}")
            db.session.rollback()
            flash('Error creating student record. Please contact the administrator.', 'error')
            return redirect(url_for('main.index'))
    
    # Get student's current courses
    courses = student.course.units.all() if student.course else []
    
    # Get student's units
    units = Unit.query.join(Course).filter(Course.id == student.course_id).all() if student.course else []
    
    # Get student's assignments
    assignments = Assignment.query.join(Unit).filter(Unit.course_id == student.course_id).all() if student.course else []
    
    # Get pending assignments (not submitted)
    pending_assignments = [a for a in assignments if not any(g.assignment_id == a.id for g in student.grades)]
    
    # Get student's grades
    grades = Grade.query.filter_by(student_id=student.id).all()
    
    # Calculate average grade
    if grades:
        average_grade = sum(g.score for g in grades) / len(grades)
    else:
        average_grade = 0
    
    # Get student's attendance
    attendance_records = Attendance.query.filter_by(student_id=student.id).all()
    
    # Calculate attendance rate
    if attendance_records:
        present_count = sum(1 for r in attendance_records if r.status == 'present')
        attendance_rate = (present_count / len(attendance_records)) * 100
    else:
        attendance_rate = 0
    
    # Get today's schedule
    today = datetime.utcnow().date()
    today_schedule = []
    
    # Get all class rooms the student is enrolled in
    class_rooms = ClassRoom.query.join(ClassRoom.students).filter(Student.id == student.id).all()
    
    for class_room in class_rooms:
        schedules = ClassSchedule.query.filter_by(class_room_id=class_room.id).all()
        for schedule in schedules:
            if schedule.day_of_week == today.strftime('%A').lower():
                today_schedule.append({
                    'unit': schedule.unit.name,
                    'start_time': schedule.start_time.strftime('%I:%M %p'),
                    'end_time': schedule.end_time.strftime('%I:%M %p'),
                    'room': class_room.room_number
                })
    
    # Sort schedule by start time
    today_schedule.sort(key=lambda x: datetime.strptime(x['start_time'], '%I:%M %p'))
    
    # Get recent activities
    recent_activities = ActivityLog.query.filter_by(student_id=student.id).order_by(ActivityLog.timestamp.desc()).limit(5).all()
    
    # Get fee balance
    fees = Fee.query.filter_by(student_id=student.id).all()
    payments = Payment.query.filter_by(student_id=student.id).all()
    
    total_fees = sum(fee.amount for fee in fees)
    total_paid = sum(payment.amount for payment in payments)
    fee_balance = total_fees - total_paid
    
    # Get current date for reports
    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    
    # Get lecturers for the student's course
    lecturers = []
    if student.course:
        lecturers = student.course.lecturers.all() if hasattr(student.course, 'lecturers') else []
    
    return render_template('student/dashboard.html',
                         student=student,
                         courses=courses,
                         units=units,
                         assignments=assignments,
                         pending_assignments=pending_assignments,
                         grades=grades,
                         average_grade=average_grade,
                         attendance_records=attendance_records,
                         attendance_rate=attendance_rate,
                         today_schedule=today_schedule,
                         recent_activities=recent_activities,
                         fee_balance=fee_balance,
                         current_date=current_date,
                         lecturers=lecturers)

@student_bp.route('/profile')
@login_required
def profile():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))
    
    return render_template('student/dashboard.html', 
                         active_tab='profile',
                         student=student)

@student_bp.route('/units')
@login_required
def units():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))
    
    # Get student's units
    units = Unit.query.join(Course).filter(Course.id == student.course_id).all() if student.course else []
    
    return render_template('student/dashboard.html',
        active_tab='units',
        student=student,
        units=units)

@student_bp.route('/register_unit', methods=['POST'])
@login_required
def register_unit():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.units'))
    
    unit_code = request.form.get('unit_code')
    unit = Unit.query.filter_by(code=unit_code).first()
    
    if not unit:
        flash('Unit not found', 'error')
        return redirect(url_for('student.units'))
    
    # Check if student is already registered for this unit
    existing_registration = UnitRegistration.query.filter_by(
        student_id=student.id,
        unit_id=unit.id
    ).first()
    
    if existing_registration:
        flash('You are already registered for this unit', 'error')
        return redirect(url_for('student.units'))
    
    # Create new registration
    registration = UnitRegistration(
        student_id=student.id,
        unit_id=unit.id,
        registration_date=datetime.now(),
        status='active'
    )
    
    db.session.add(registration)
    db.session.commit()
    
    flash('Unit registered successfully', 'success')
    return redirect(url_for('student.units'))

@student_bp.route('/results')
@login_required
def results():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))
    
    # Get all grades for this student with unit and course information
    grades = Grade.query.filter_by(student_id=student.id).join(Unit).join(Course).all()
    
    # Calculate statistics
    total_units = len(grades)
    graded_units = len([g for g in grades if g.score is not None])
    average_score = sum(g.score for g in grades if g.score is not None) / graded_units if graded_units > 0 else 0
    
    # Grade distribution
    grade_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for grade in grades:
        if grade.grade_letter and grade.grade_letter in grade_distribution:
            grade_distribution[grade.grade_letter] += 1
    
    # Get course units for comparison
    course_units = Unit.query.filter_by(course_id=student.course_id).all() if student.course else []
    ungraded_units = [unit for unit in course_units if not any(g.unit_id == unit.id for g in grades)]
    
    # Get lecturers for the student's course
    lecturers = []
    if student.course:
        lecturers = student.course.lecturers.all() if hasattr(student.course, 'lecturers') else []
    
    return render_template('student/dashboard.html',
        active_tab='results',
        student=student,
        grades=grades,
        total_units=total_units,
        graded_units=graded_units,
        average_score=average_score,
        grade_distribution=grade_distribution,
        ungraded_units=ungraded_units,
        course_units=course_units,
        lecturers=lecturers)

@student_bp.route('/download_results')
@login_required
def download_results():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))
    
    results = Grade.query.filter_by(student_id=student.id).all()
    
    # Create CSV file
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Unit Code', 'Unit Name', 'Score (%)', 'Grade Letter', 'Remarks', 'Date'])
    
    for result in results:
        cw.writerow([
            result.unit.code if result.unit else 'N/A',
            result.unit.name if result.unit else 'N/A',
            f"{result.score:.1f}" if result.score is not None else 'N/A',
            result.grade_letter or 'N/A',
            result.remarks or 'N/A',
            result.created_at.strftime('%Y-%m-%d') if result.created_at else 'N/A'
        ])
    
    output = si.getvalue()
    si.close()
    
    return send_file(
        BytesIO(output.encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'results_{student.student_number}.csv'
    )

@student_bp.route('/fees')
@login_required
def fees():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))

    # Auto-generate fees from fee structure if not already created
    if student.course:
        fee_structures = FeeStructure.query.filter_by(course_id=student.course_id).all()
        updated_fees = False
        for fs in fee_structures:
            existing_fee = Fee.query.filter_by(
                student_id=student.id,
                fee_structure_id=fs.id
            ).first()
            
            if not existing_fee:
                new_fee = Fee(
                    student_id=student.id,
                    fee_structure_id=fs.id,
                    academic_year=fs.academic_year,
                    semester=fs.semester,
                    amount=fs.amount,
                    due_date=fs.due_date.date() if fs.due_date else datetime.now().date(),
                    status='pending'
                )
                db.session.add(new_fee)
                updated_fees = True
            elif existing_fee.amount != fs.amount:
                current_app.logger.info(f'Updating fee for student {student.id} from {existing_fee.amount} to {fs.amount}')
                existing_fee.amount = fs.amount
                existing_fee.updated_at = datetime.utcnow()
                updated_fees = True
        
        # Commit any new fees to the database
        if updated_fees:
            db.session.commit()

    # Get comprehensive fee summary
    fee_summary = Fee.get_student_fees_summary(student.id)
    
    # Get payment history
    payment_history = Payment.get_student_payment_history(student.id)
    
    return render_template('student/fees.html', 
                           fee_summary=fee_summary,
                           payment_history=payment_history,
                           student=student)

@student_bp.route('/download_fee_structure')
@login_required
def download_fee_structure():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))
    
    fee_structure = FeeStructure.query.filter_by(course_id=student.course_id).all() if student.course else []
    
    # Create CSV file
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Fee Type', 'Amount', 'Due Date', 'Description'])
    
    for fee in fee_structure:
        cw.writerow([
            fee.type,
            fee.amount,
            fee.due_date.strftime('%Y-%m-%d') if fee.due_date else 'N/A',
            fee.description or 'N/A'
        ])
    
    output = si.getvalue()
    si.close()
    
    return send_file(
        StringIO(output),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'fee_structure_{student.course.code if student.course else "unknown"}.csv'
    )

@student_bp.route('/make_payment', methods=['POST'])
@login_required
def make_payment():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.fees'))
    
    payment_type = request.form.get('payment_type')
    amount = float(request.form.get('amount'))
    payment_method = request.form.get('payment_method')
    
    # Create payment record
    payment = Payment(
        student_id=student.id,
        amount=amount,
        payment_type=payment_type,
        payment_method=payment_method,
        payment_date=datetime.now(),
        status='pending'
    )
    
    db.session.add(payment)
    db.session.commit()
    
    # Here you would typically integrate with a payment gateway
    # For now, we'll just mark it as successful
    payment.status = 'completed'
    db.session.commit()
    
    flash('Payment processed successfully', 'success')
    return redirect(url_for('student.fees'))

@student_bp.route('/assignments')
@login_required
def assignments():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))
    
    assignments = Assignment.query.filter_by(student_id=student.id).all()
    return render_template('student/dashboard.html',
        active_tab='assignments',
        student=student,
        assignments=assignments
    )

@student_bp.route('/attendance')
@login_required
def attendance():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))
    
    attendance_records = Attendance.query.filter_by(student_id=student.id).all()
    return render_template('student/dashboard.html',
        active_tab='attendance',
        student=student,
        attendance_records=attendance_records
    )

@student_bp.route('/timetable')
@login_required
def timetable():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))
    
    # For now, get all class schedules since student_id doesn't exist in ClassSchedule
    schedule = ClassSchedule.query.all()
    return render_template('student/dashboard.html',
        active_tab='timetable',
        student=student,
        schedule=schedule
    )

@student_bp.route('/exam-results')
@login_required
def exam_results():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))
    
    # Get all exam results for the student
    results = ExamResult.query.filter_by(student_id=student.id).all()
    
    # For now, group results by exam title since academic_year/semester don't exist
    results_by_exam = {}
    for result in results:
        exam_title = result.exam.title if result.exam else 'Unknown Exam'
        if exam_title not in results_by_exam:
            results_by_exam[exam_title] = []
        results_by_exam[exam_title].append(result)
    
    return render_template('student/exam_results.html',
                         results_by_exam=results_by_exam)

@student_bp.route('/generate-result-slip/<academic_year>/<semester>')
@login_required
def generate_result_slip(academic_year, semester):
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))
    
    # Get exam results for the student (without academic_year/semester filter for now)
    results = ExamResult.query.filter(
        ExamResult.student_id == student.id
    ).all()
    
    return render_template('student/result_slip.html',
                         student=student,
                         results=results,
                         academic_year=academic_year,
                         semester=semester,
                         current_date=datetime.utcnow())

@student_bp.route('/reports')
@login_required
def reports():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))
    
    return render_template('student/dashboard.html',
                         active_tab='reports',
                         student=student)

@student_bp.route('/generate-report', methods=['POST'])
@login_required
def generate_report():
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        return jsonify({'error': 'Student record not found'}), 404
    
    report_type = request.form.get('reportType')
    year = request.form.get('year')
    semester = request.form.get('semester')
    
    if report_type == 'result_slip':
        # Get grades for the student (without year/semester filter for now)
        grades = Grade.query.filter(
            Grade.student_id == student.id
        ).all()
        
        # Calculate overall grade
        overall_grade = sum(grade.score for grade in grades) / len(grades) if grades else 0
        
        return render_template('student/reports/result_slip.html',
                             student=student,
                             grades=grades,
                             year=year,
                             semester=semester,
                             overall_grade=overall_grade)
    
    elif report_type == 'fee_statement':
        # Get fee structure and payments for the student (without year filter for now)
        fee_structure = FeeStructure.query.filter_by(
            course_id=student.course.id
        ).all() if student.course else []
        
        payments = Payment.query.filter(
            Payment.student_id == student.id
        ).all()
        
        return render_template('student/reports/fee_statement.html',
                             student=student,
                             fee_structure=fee_structure,
                             payments=payments,
                             year=year)
    
    elif report_type == 'attendance_record':
        # Get attendance records for the student (without year/semester filter for now)
        attendance_records = Attendance.query.filter(
            Attendance.student_id == student.id
        ).all()
        
        return render_template('student/reports/attendance_record.html',
                             student=student,
                             attendance_records=attendance_records,
                             year=year,
                             semester=semester)
    
    return jsonify({'error': 'Invalid report type'}), 400

@student_bp.route('/generate-fee-statement')
@login_required
def generate_fee_statement():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))
    
    # Get fee structure and payments
    fee_structure = FeeStructure.query.filter_by(
        course_id=student.course_id
    ).all() if student.course else []
    
    payments = Payment.query.filter_by(student_id=student.id).all()
    
    # Calculate totals
    total_fees = sum(fee.amount for fee in fee_structure)
    total_paid = sum(payment.amount for payment in payments)
    balance = total_fees - total_paid
    
    return render_template('student/reports/fee_statement.html',
                         student=student,
                         fee_structure=fee_structure,
                         payments=payments,
                         total_fees=total_fees,
                         total_paid=total_paid,
                         balance=balance,
                         current_date=datetime.utcnow())

@student_bp.route('/generate-attendance-record')
@login_required
def generate_attendance_record():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))
    
    # Get attendance records
    attendance_records = Attendance.query.filter_by(student_id=student.id).all()
    
    # Calculate attendance statistics
    total_sessions = len(attendance_records)
    present_count = sum(1 for record in attendance_records if record.status == 'present')
    absent_count = sum(1 for record in attendance_records if record.status == 'absent')
    late_count = sum(1 for record in attendance_records if record.status == 'late')
    attendance_rate = (present_count / total_sessions * 100) if total_sessions > 0 else 0
    
    return render_template('student/reports/attendance_record.html',
                         student=student,
                         attendance_records=attendance_records,
                         total_sessions=total_sessions,
                         present_count=present_count,
                         absent_count=absent_count,
                         late_count=late_count,
                         attendance_rate=attendance_rate,
                         current_date=datetime.utcnow())

@student_bp.route('/download_results_pdf')
@login_required
def download_results_pdf():
    # Get student record
    student = Student.query.filter_by(email=current_user.email).first()
    if not student:
        flash('Student record not found. Please contact the administrator.', 'error')
        return redirect(url_for('student.dashboard'))

    # Get grades for the student
    results = Grade.query.filter_by(student_id=student.id).all()

    # Create PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, "KITELAKPEL TECHNICAL TRAINING INSTITUTE")
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width / 2, height - 80, "Academic Results Slip")

    # Student Info
    p.setFont("Helvetica", 12)
    y = height - 120
    p.drawString(50, y, f"Name: {student.first_name} {student.last_name}")
    y -= 20
    p.drawString(50, y, f"Student Number: {student.student_number}")
    y -= 20
    p.drawString(50, y, f"Course: {student.course.name if student.course else 'N/A'}")
    y -= 20
    p.drawString(50, y, f"Email: {student.email}")

    # Table Header
    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Unit Code")
    p.drawString(120, y, "Unit Name")
    p.drawString(300, y, "Score (%)")
    p.drawString(380, y, "Grade")
    p.drawString(430, y, "Remarks")

    # Table Content
    p.setFont("Helvetica", 12)
    y -= 20
    for result in results:
        if y < 80:  # New page if needed
            p.showPage()
            y = height - 50
        p.drawString(50, y, f"{result.unit.code if result.unit else 'N/A'}")
        p.drawString(120, y, f"{result.unit.name if result.unit else 'N/A'}")
        p.drawString(300, y, f"{result.score if result.score is not None else 'N/A'}")
        p.drawString(380, y, f"{result.grade_letter or 'N/A'}")
        p.drawString(430, y, f"{result.remarks or ''}")
        y -= 20

    # Footer
    from datetime import datetime
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 40, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(50, 25, "This is a computer-generated document and does not require a signature.")

    p.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'results_{student.student_number}.pdf',
        mimetype='application/pdf'
    )

# Temporarily comment out routes that depend on non-existent models
"""
@student_bp.route('/results')
@login_required
def results():
    academic_year = request.args.get('academic_year', datetime.now().year)
    semester = request.args.get('semester', 'First Semester')
    
    results = ExamResult.query.filter_by(
        student_id=current_user.id,
        academic_year=academic_year,
        semester=semester
    ).all()
    
    return render_template('student/results.html',
                         results=results,
                         academic_year=academic_year,
                         semester=semester)

@student_bp.route('/download-results')
@login_required
def download_results():
    if not PDFKIT_AVAILABLE:
        flash('PDF generation is not available. Please contact support.', 'error')
        return redirect(url_for('student.results'))
    
    academic_year = request.args.get('academic_year', datetime.now().year)
    semester = request.args.get('semester', 'First Semester')
    
    results = ExamResult.query.filter_by(
        student_id=current_user.id,
        academic_year=academic_year,
        semester=semester
    ).all()
    
    # Generate HTML
    html = render_template('student/results_pdf.html',
                         student=current_user,
                         results=results,
                         academic_year=academic_year,
                         semester=semester)
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        try:
            # Configure pdfkit options
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': 'UTF-8',
                'no-outline': None
            }
            
            # Generate PDF
            pdfkit.from_string(html, tmp.name, options=options)
            
            # Send file
            return send_file(
                tmp.name,
                as_attachment=True,
                download_name=f'results_{academic_year}_{semester}.pdf',
                mimetype='application/pdf'
            )
        except Exception as e:
            flash('Error generating PDF. Please try again.', 'error')
            return redirect(url_for('student.results'))
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp.name)
            except:
                pass

@student_bp.route('/fees')
@login_required
def fees():
    academic_year = request.args.get('academic_year', datetime.now().year)
    semester = request.args.get('semester', 'First Semester')
    
    fees = Fee.query.filter_by(
        student_id=current_user.id,
        academic_year=academic_year,
        semester=semester
    ).all()
    
    total_fees = sum(fee.amount for fee in fees)
    total_paid = sum(payment.amount for fee in fees for payment in fee.payments if payment.status == 'completed')
    balance = total_fees - total_paid
    
    payments = Payment.query.join(Fee).filter(
        Fee.student_id == current_user.id,
        Fee.academic_year == academic_year,
        Fee.semester == semester
    ).order_by(Payment.payment_date.desc()).all()
    
    return render_template('student/fees.html',
                         fees=fees,
                         payments=payments,
                         total_fees=total_fees,
                         total_paid=total_paid,
                         balance=balance,
                         academic_year=academic_year,
                         semester=semester)

@student_bp.route('/unit-registration')
@login_required
def unit_registration():
    # Get current registration period
    current_period = RegistrationPeriod.query.filter_by(is_active=True).first()
    
    # Get student's course
    student_course = current_user.course
    
    # Get available units for the student's course
    available_units = Module.query.filter_by(course_id=student_course.id).all()
    
    # Get student's registered units
    registered_units = UnitRegistration.query.filter_by(
        student_id=current_user.id
    ).order_by(UnitRegistration.created_at.desc()).all()
    
    return render_template('student/unit_registration.html',
                         current_period=current_period,
                         available_units=available_units,
                         registered_units=registered_units)

@student_bp.route('/register-units', methods=['POST'])
@login_required
def register_units():
    # Check if registration period is open
    current_period = RegistrationPeriod.query.filter_by(is_active=True).first()
    if not current_period:
        flash('Registration period is not open.', 'error')
        return redirect(url_for('student.unit_registration'))
    
    # Get selected units
    selected_units = request.form.getlist('units')
    if not selected_units:
        flash('Please select at least one unit.', 'error')
        return redirect(url_for('student.unit_registration'))
    
    # Get student's course
    student_course = current_user.course
    
    # Verify all selected units belong to student's course
    valid_units = Module.query.filter(
        Module.id.in_(selected_units),
        Module.course_id == student_course.id
    ).all()
    
    if len(valid_units) != len(selected_units):
        flash('Invalid unit selection.', 'error')
        return redirect(url_for('student.unit_registration'))
    
    # Check if already registered for any of these units in the current period
    existing_registrations = UnitRegistration.query.filter(
        UnitRegistration.student_id == current_user.id,
        UnitRegistration.unit_id.in_(selected_units),
        UnitRegistration.academic_year == current_period.academic_year,
        UnitRegistration.semester == current_period.semester
    ).all()
    
    if existing_registrations:
        flash('You have already registered for some of these units.', 'error')
        return redirect(url_for('student.unit_registration'))
    
    # Create registrations
    for unit in valid_units:
        registration = UnitRegistration(
            student_id=current_user.id,
            unit_id=unit.id,
            academic_year=current_period.academic_year,
            semester=current_period.semester,
            status='pending'
        )
        db.session.add(registration)
    
    try:
        db.session.commit()
        flash('Units registered successfully. Waiting for approval.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error registering units. Please try again.', 'error')
    
    return redirect(url_for('student.unit_registration'))
""" 