from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, make_response
from flask_login import login_required, current_user
from app.models import Course, ClassRoom, Assignment, Grade, Attendance, TeachingMaterial, User, Unit, Student, Enrollment
from app import db
from datetime import datetime, timedelta
import os

bp = Blueprint('lecturer', __name__, url_prefix='/lecturer')

@bp.before_request
def before_request():
    if not current_user.is_authenticated or current_user.role != 'lecturer':
        flash('Access denied. Lecturer access required.', 'danger')
        return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get lecturer's courses (many-to-many)
    courses = current_user.courses_teaching.all()
    
    # Get lecturer's classes
    classes = ClassRoom.query.filter_by(lecturer_id=current_user.id).all()
    
    # Get today's schedule
    today = datetime.now().strftime('%A')
    today_schedule = ClassRoom.query.filter_by(
        lecturer_id=current_user.id,
        day=today
    ).order_by(ClassRoom.start_time).all()
    
    # Get recent activities (flattened for template)
    recent = get_recent_activities()
    recent_activities = []
    for grade in recent['grades']:
        recent_activities.append({
            'title': f"Graded: {grade.unit.name if grade.unit else 'Unknown Unit'}",
            'description': f"Graded {grade.student.first_name} {grade.student.last_name} - Score: {grade.score}%",
            'timestamp': grade.created_at
        })
    for assignment in recent['assignments']:
        recent_activities.append({
            'title': f"New Assignment: {assignment.title}",
            'description': assignment.description,
            'timestamp': assignment.created_at
        })
    for attendance in recent['attendance']:
        recent_activities.append({
            'title': f"Attendance Taken: {attendance.class_room.name}",
            'description': f"Attendance for {attendance.date.strftime('%Y-%m-%d')}",
            'timestamp': attendance.date
        })
    # Sort all activities by timestamp descending
    recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Get statistics
    total_students = 0
    for course in courses:
        # Get students through many-to-many relationship (enrollments)
        students_m2m = course.students.all()
        
        # Get students through direct relationship (course_id in students table)
        students_direct = Student.query.filter_by(course_id=course.id).all()
        
        # Combine both lists and remove duplicates
        course_students = list(students_m2m)
        for student in students_direct:
            if student not in course_students:
                course_students.append(student)
        
        total_students += len(course_students)
    
    active_classes = len(classes)
    total_courses = len(courses)
    total_units = sum(len(course.units.all()) for course in courses)
    pending_tasks = get_pending_tasks()
    
    return render_template('lecturer/dashboard.html',
                         courses=courses,
                         classes=classes,
                         today_schedule=today_schedule,
                         recent_activities=recent_activities,
                         total_students=total_students,
                         active_classes=active_classes,
                         total_courses=total_courses,
                         total_units=total_units,
                         pending_tasks=pending_tasks)

@bp.route('/courses')
@login_required
def courses():
    courses = current_user.courses_teaching.all()
    return render_template('lecturer/courses.html', courses=courses)

@bp.route('/courses/<int:course_id>/units')
@login_required
def view_course_units(course_id):
    course = Course.query.get_or_404(course_id)
    # Check if lecturer is assigned to this course
    if course not in current_user.courses_teaching:
        flash('Access denied. You are not assigned to this course.', 'danger')
        return redirect(url_for('lecturer.courses'))
    units = course.units.all()
    return render_template('lecturer/course_units.html', course=course, units=units)

@bp.route('/units')
@login_required
def units():
    courses = current_user.courses_teaching.all()
    all_units = []
    for course in courses:
        course_units = course.units.all()
        for unit in course_units:
            all_units.append({'unit': unit, 'course': course})
    return render_template('lecturer/units.html', units=all_units)

@bp.route('/grading')
@login_required
def grading():
    courses = current_user.courses_teaching.all()
    return render_template('lecturer/grading.html', courses=courses)

@bp.route('/grading/course/<int:course_id>')
@login_required
def course_grading(course_id):
    course = Course.query.get_or_404(course_id)
    if course not in current_user.courses_teaching:
        flash('Access denied. You are not assigned to this course.', 'danger')
        return redirect(url_for('lecturer.grading'))
    
    # Get students through many-to-many relationship (enrollments)
    students_m2m = course.students.all()
    
    # Get students through direct relationship (course_id in students table)
    students_direct = Student.query.filter_by(course_id=course.id).all()
    
    # Combine both lists and remove duplicates
    students = list(students_m2m)
    for student in students_direct:
        if student not in students:
            students.append(student)
    
    units = course.units.all()
    grades = {}
    for student in students:
        grades[student.id] = {}
        for unit in units:
            grade = Grade.query.filter_by(student_id=student.id, unit_id=unit.id).first()
            grades[student.id][unit.id] = grade
    return render_template('lecturer/course_grading.html', course=course, students=students, units=units, grades=grades)

@bp.route('/grading/unit/<int:unit_id>')
@login_required
def unit_grading(unit_id):
    unit = Unit.query.get_or_404(unit_id)
    course = unit.course
    if course not in current_user.courses_teaching:
        flash('Access denied. You are not assigned to this unit.', 'danger')
        return redirect(url_for('lecturer.grading'))
    
    # Get students through many-to-many relationship (enrollments)
    students_m2m = course.students.all()
    
    # Get students through direct relationship (course_id in students table)
    students_direct = Student.query.filter_by(course_id=course.id).all()
    
    # Combine both lists and remove duplicates
    students = list(students_m2m)
    for student in students_direct:
        if student not in students:
            students.append(student)
    
    grades = {}
    for student in students:
        grade = Grade.query.filter_by(student_id=student.id, unit_id=unit.id).first()
        grades[student.id] = grade
    return render_template('lecturer/unit_grading.html', unit=unit, course=course, students=students, grades=grades)

@bp.route('/grading/update', methods=['POST'])
@login_required
def update_grade():
    """Update or create a grade for a student"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        unit_id = data.get('unit_id')
        score = data.get('score')
        remarks = data.get('remarks', '')
        
        # Validate data
        if not all([student_id, unit_id, score]):
            return jsonify({'success': False, 'message': 'Missing required data'}), 400
        
        # Check if lecturer is assigned to this unit
        unit = Unit.query.get_or_404(unit_id)
        if unit.course not in current_user.courses_teaching:
            return jsonify({'success': False, 'message': 'Access denied'}), 403
        
        # Check if student is enrolled in this course
        student = Student.query.get_or_404(student_id)
        if student.course_id != unit.course.id:
            return jsonify({'success': False, 'message': 'Student not enrolled in this course'}), 400
        
        # Validate score
        try:
            score = float(score)
            if score < 0 or score > 100:
                return jsonify({'success': False, 'message': 'Score must be between 0 and 100'}), 400
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid score format'}), 400
        
        # Determine grade letter
        grade_letter = get_grade_letter(score)
        
        # Check if grade already exists
        existing_grade = Grade.query.filter_by(student_id=student_id, unit_id=unit_id).first()
        
        if existing_grade:
            # Update existing grade
            existing_grade.score = score
            existing_grade.grade_letter = grade_letter
            existing_grade.remarks = remarks
            existing_grade.updated_at = datetime.utcnow()
            message = 'Grade updated successfully'
        else:
            # Create new grade
            new_grade = Grade(
                student_id=student_id,
                unit_id=unit_id,
                score=score,
                grade_letter=grade_letter,
                remarks=remarks
            )
            db.session.add(new_grade)
            message = 'Grade created successfully'
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': message,
            'grade_letter': grade_letter,
            'score': score
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@bp.route('/grading/bulk-update', methods=['POST'])
@login_required
def bulk_update_grades():
    """Bulk update grades for multiple students"""
    try:
        data = request.get_json()
        unit_id = data.get('unit_id')
        grades_data = data.get('grades', [])
        
        if not unit_id or not grades_data:
            return jsonify({'success': False, 'message': 'Missing required data'}), 400
        
        # Check if lecturer is assigned to this unit
        unit = Unit.query.get_or_404(unit_id)
        if unit.course not in current_user.courses_teaching:
            return jsonify({'success': False, 'message': 'Access denied'}), 403
        
        updated_count = 0
        created_count = 0
        
        for grade_data in grades_data:
            student_id = grade_data.get('student_id')
            score = grade_data.get('score')
            remarks = grade_data.get('remarks', '')
            
            if not student_id or score is None:
                continue
            
            # Validate score
            try:
                score = float(score)
                if score < 0 or score > 100:
                    continue
            except ValueError:
                continue
            
            # Check if student is enrolled in this course
            student = Student.query.get(student_id)
            if not student or student.course_id != unit.course.id:
                continue
            
            # Determine grade letter
            grade_letter = get_grade_letter(score)
            
            # Check if grade already exists
            existing_grade = Grade.query.filter_by(student_id=student_id, unit_id=unit_id).first()
            
            if existing_grade:
                # Update existing grade
                existing_grade.score = score
                existing_grade.grade_letter = grade_letter
                existing_grade.remarks = remarks
                existing_grade.updated_at = datetime.utcnow()
                updated_count += 1
            else:
                # Create new grade
                new_grade = Grade(
                    student_id=student_id,
                    unit_id=unit_id,
                    score=score,
                    grade_letter=grade_letter,
                    remarks=remarks
                )
                db.session.add(new_grade)
                created_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Grades updated successfully. {created_count} created, {updated_count} updated.'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@bp.route('/grading/student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def student_grading(student_id):
    """View and grade a specific student"""
    student = Student.query.get_or_404(student_id)
    
    # Check if lecturer is assigned to this student's course
    if student.course not in current_user.courses_teaching:
        flash('Access denied. You are not assigned to this student.', 'danger')
        return redirect(url_for('lecturer.grading'))
    
    # Get all units for this course
    units = student.course.units.all()
    
    if request.method == 'POST':
        # Handle form submission for saving grades
        try:
            for unit in units:
                score_key = f'score_{unit.id}'
                remarks_key = f'remarks_{unit.id}'
                
                score = request.form.get(score_key)
                remarks = request.form.get(remarks_key, '')
                
                if score and score.strip():  # Only process if score is provided
                    try:
                        score = float(score)
                        if score < 0 or score > 100:
                            flash(f'Score for {unit.name} must be between 0 and 100.', 'danger')
                            continue
                    except ValueError:
                        flash(f'Invalid score format for {unit.name}.', 'danger')
                        continue
                    
                    # Determine grade letter
                    grade_letter = get_grade_letter(score)
                    
                    # Check if grade already exists
                    existing_grade = Grade.query.filter_by(student_id=student.id, unit_id=unit.id).first()
                    
                    if existing_grade:
                        # Update existing grade
                        existing_grade.score = score
                        existing_grade.grade_letter = grade_letter
                        existing_grade.remarks = remarks
                        existing_grade.updated_at = datetime.utcnow()
                    else:
                        # Create new grade
                        new_grade = Grade(
                            student_id=student.id,
                            unit_id=unit.id,
                            score=score,
                            grade_letter=grade_letter,
                            remarks=remarks
                        )
                        db.session.add(new_grade)
            
            db.session.commit()
            flash('Grades saved successfully!', 'success')
            return redirect(url_for('lecturer.student_grading', student_id=student.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving grades: {str(e)}', 'danger')
    
    # Get existing grades for this student
    grades = {}
    for unit in units:
        grade = Grade.query.filter_by(student_id=student.id, unit_id=unit.id).first()
        grades[unit.id] = grade
    
    return render_template('lecturer/student_grading.html', 
                         student=student, 
                         units=units, 
                         grades=grades)

@bp.route('/grading/reports')
@login_required
def grading_reports():
    """View grading reports and statistics"""
    courses = current_user.courses_teaching.all()
    
    reports = []
    for course in courses:
        students = course.students.all()
        units = course.units.all()
        
        course_stats = {
            'course': course,
            'total_students': len(students),
            'total_units': len(units),
            'graded_units': 0,
            'average_score': 0,
            'grade_distribution': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        }
        
        total_scores = 0
        total_grades = 0
        
        for unit in units:
            unit_grades = Grade.query.filter_by(unit_id=unit.id).all()
            if unit_grades:
                course_stats['graded_units'] += 1
                for grade in unit_grades:
                    total_scores += grade.score
                    total_grades += 1
                    if grade.grade_letter in course_stats['grade_distribution']:
                        course_stats['grade_distribution'][grade.grade_letter] += 1
        
        if total_grades > 0:
            course_stats['average_score'] = round(total_scores / total_grades, 2)
        
        reports.append(course_stats)
    
    return render_template('lecturer/grading_reports.html', reports=reports)

def get_grade_letter(score):
    """Convert numerical score to grade letter"""
    if score >= 80:
        return 'A'
    elif score >= 70:
        return 'B'
    elif score >= 60:
        return 'C'
    elif score >= 50:
        return 'D'
    else:
        return 'F'

@bp.route('/classes')
@login_required
def classes():
    classes = ClassRoom.query.filter_by(lecturer_id=current_user.id).all()
    return render_template('lecturer/classes.html', classes=classes)

@bp.route('/attendance/<int:class_id>', methods=['GET', 'POST'])
@login_required
def attendance(class_id):
    class_obj = ClassRoom.query.get_or_404(class_id)
    if class_obj.lecturer_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('lecturer.dashboard'))
        
    if request.method == 'POST':
        data = request.get_json()
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        attendance_data = data.get('attendance')
        
        # Save attendance records
        for student_id, status in attendance_data.items():
            attendance = Attendance(
                student_id=student_id,
                class_id=class_id,
                date=date,
                status=status
            )
            db.session.add(attendance)
            
        db.session.commit()
        return jsonify({'message': 'Attendance recorded successfully'})
        
    # Get attendance records
    attendance_records = Attendance.query.filter_by(class_id=class_id).order_by(Attendance.date.desc()).all()
    return render_template('lecturer/attendance.html', class_obj=class_obj, attendance_records=attendance_records)

@bp.route('/assignments', methods=['GET', 'POST'])
@login_required
def assignments():
    if request.method == 'POST':
        data = request.form
        assignment = Assignment(
            title=data.get('title'),
            description=data.get('description'),
            class_id=data.get('class_id'),
            due_date=datetime.strptime(data.get('due_date'), '%Y-%m-%d'),
            lecturer_id=current_user.id
        )
        db.session.add(assignment)
        db.session.commit()
        flash('Assignment created successfully.', 'success')
        return redirect(url_for('lecturer.assignments'))
        
    assignments = Assignment.query.filter_by(lecturer_id=current_user.id).all()
    classes = ClassRoom.query.filter_by(lecturer_id=current_user.id).all()
    return render_template('lecturer/assignments.html', assignments=assignments, classes=classes)

@bp.route('/grades', methods=['GET', 'POST'])
@login_required
def grades():
    if request.method == 'POST':
        data = request.form
        grade = Grade(
            student_id=data.get('student_id'),
            assignment_id=data.get('assignment_id'),
            grade=data.get('grade'),
            comments=data.get('comments')
        )
        db.session.add(grade)
        db.session.commit()
        flash('Grade recorded successfully.', 'success')
        return redirect(url_for('lecturer.grades'))
        
    grades = Grade.query.join(Assignment).filter(Assignment.lecturer_id == current_user.id).all()
    return render_template('lecturer/grades.html', grades=grades)

@bp.route('/materials', methods=['GET', 'POST'])
@login_required
def materials():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            
            material = TeachingMaterial(
                title=request.form.get('title'),
                description=request.form.get('description'),
                file_path=filename,
                lecturer_id=current_user.id,
                class_id=request.form.get('class_id')
            )
            db.session.add(material)
            db.session.commit()
            flash('Material uploaded successfully.', 'success')
            return redirect(url_for('lecturer.materials'))
            
    materials = TeachingMaterial.query.filter_by(lecturer_id=current_user.id).all()
    classes = ClassRoom.query.filter_by(lecturer_id=current_user.id).all()
    return render_template('lecturer/materials.html', materials=materials, classes=classes)

@bp.route('/timetable')
@login_required
def timetable():
    timetable = ClassRoom.query.filter_by(lecturer_id=current_user.id).all()
    return render_template('lecturer/timetable.html', timetable=timetable)

@bp.route('/reports')
@login_required
def reports():
    # Get attendance statistics
    attendance_stats = get_attendance_statistics()
    
    # Get grade distribution
    grade_distribution = get_grade_distribution()
    
    # Get class performance
    class_performance = get_class_performance()
    
    return render_template('lecturer/reports.html',
                         attendance_stats=attendance_stats,
                         grade_distribution=grade_distribution,
                         class_performance=class_performance)

@bp.route('/export/attendance')
@login_required
def export_attendance():
    # Get attendance records for all classes
    attendance_records = Attendance.query.join(ClassRoom)\
        .filter(ClassRoom.lecturer_id == current_user.id)\
        .order_by(Attendance.date.desc()).all()
    
    # Create CSV data
    csv_data = "Date,Class,Student,Status\n"
    for record in attendance_records:
        csv_data += f"{record.date.strftime('%Y-%m-%d')},{record.class_room.name},{record.student.first_name} {record.student.last_name},{record.status}\n"
    
    # Create response
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=attendance_report.csv"
    response.headers["Content-type"] = "text/csv"
    return response

@bp.route('/export/grades')
@login_required
def export_grades():
    # Get grades for all assignments
    grades = Grade.query.join(Assignment)\
        .filter(Assignment.lecturer_id == current_user.id)\
        .order_by(Grade.created_at.desc()).all()
    
    # Create CSV data
    csv_data = "Assignment,Student,Score,Grade Letter,Remarks,Created At\n"
    for grade in grades:
        csv_data += f"{grade.assignment.title},{grade.student.first_name} {grade.student.last_name},{grade.score},{grade.grade_letter or 'N/A'},{grade.remarks or 'N/A'},{grade.created_at.strftime('%Y-%m-%d %H:%M')}\n"
    
    # Create response
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=grades_report.csv"
    response.headers["Content-type"] = "text/csv"
    return response

@bp.route('/export/performance')
@login_required
def export_performance():
    # Get performance data
    attendance_stats = get_attendance_statistics()
    grade_distribution = get_grade_distribution()
    class_performance = get_class_performance()
    
    # Create CSV data
    csv_data = "Report Type,Class,Value\n"
    
    # Add attendance statistics
    for class_name, rate in attendance_stats.items():
        csv_data += f"Attendance,{class_name},{rate}\n"
    
    # Add grade distribution
    for assignment, stats in grade_distribution.items():
        csv_data += f"Grade Distribution,{assignment},Average: {stats['average']}, Highest: {stats['highest']}, Lowest: {stats['lowest']}\n"
    
    # Add class performance
    for class_name, performance in class_performance.items():
        csv_data += f"Class Performance,{class_name},Average: {performance['average']}, Passing Rate: {performance['passing_rate']}\n"
    
    # Create response
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=performance_report.csv"
    response.headers["Content-type"] = "text/csv"
    return response

# Helper functions
def get_recent_activities():
    # Get recent grades
    recent_grades = Grade.query.join(Unit).join(Course)\
        .filter(Course.lecturer_id == current_user.id)\
        .order_by(Grade.created_at.desc()).limit(5).all()
    
    # Get recent assignments
    recent_assignments = Assignment.query\
        .filter_by(lecturer_id=current_user.id)\
        .order_by(Assignment.created_at.desc()).limit(5).all()
    
    # Get recent attendance records
    recent_attendance = Attendance.query.join(ClassRoom)\
        .filter(ClassRoom.lecturer_id == current_user.id)\
        .order_by(Attendance.date.desc()).limit(5).all()
    
    return {
        'grades': recent_grades,
        'assignments': recent_assignments,
        'attendance': recent_attendance
    }

def get_pending_tasks():
    tasks = []
    
    # Pending assignments to grade
    pending_grades = Assignment.query.filter_by(lecturer_id=current_user.id)\
        .filter(Assignment.due_date < datetime.now())\
        .filter(~Assignment.grades.any()).all()
    for assignment in pending_grades:
        tasks.append({
            'title': f'Grade Assignment: {assignment.title}',
            'description': f'Due: {assignment.due_date.strftime("%Y-%m-%d")}',
            'due_date': assignment.due_date,
            'link': url_for('lecturer.grades')
        })
    
    # Upcoming assignments to create
    upcoming_classes = ClassRoom.query.filter_by(lecturer_id=current_user.id)\
        .filter(ClassRoom.start_time > datetime.now())\
        .filter(ClassRoom.start_time < datetime.now() + timedelta(days=7)).all()
    for class_obj in upcoming_classes:
        tasks.append({
            'title': f'Prepare for Class: {class_obj.name}',
            'description': f'Scheduled: {class_obj.start_time.strftime("%Y-%m-%d %H:%M")}',
            'due_date': class_obj.start_time,
            'link': url_for('lecturer.classes')
        })
    
    return tasks

def get_attendance_statistics():
    # Get attendance statistics for all classes
    stats = {}
    classes = ClassRoom.query.filter_by(lecturer_id=current_user.id).all()
    
    for class_obj in classes:
        attendance_records = Attendance.query.filter_by(class_id=class_obj.id).all()
        total_sessions = len(attendance_records)
        if total_sessions > 0:
            present_count = sum(1 for record in attendance_records if record.status == 'present')
            attendance_rate = (present_count / total_sessions) * 100
            stats[class_obj.name] = attendance_rate
    
    return stats

def get_grade_distribution():
    # Get grade distribution for all assignments
    distribution = {}
    assignments = Assignment.query.filter_by(lecturer_id=current_user.id).all()
    
    for assignment in assignments:
        grades = [grade.score for grade in assignment.grades]
        if grades:
            distribution[assignment.title] = {
                'average': sum(grades) / len(grades),
                'highest': max(grades),
                'lowest': min(grades)
            }
    
    return distribution

def get_class_performance():
    # Get overall class performance metrics
    performance = {}
    classes = ClassRoom.query.filter_by(lecturer_id=current_user.id).all()
    
    for class_obj in classes:
        assignments = Assignment.query.filter_by(class_id=class_obj.id).all()
        if assignments:
            all_grades = []
            for assignment in assignments:
                all_grades.extend([grade.score for grade in assignment.grades])
            
            if all_grades:
                performance[class_obj.name] = {
                    'average': sum(all_grades) / len(all_grades),
                    'passing_rate': (sum(1 for grade in all_grades if grade >= 60) / len(all_grades)) * 100
                }
    
    return performance

@bp.route('/my_students')
@login_required
def my_students():
    courses = current_user.courses_teaching.all()
    course_students = {}
    
    for course in courses:
        # Get students through many-to-many relationship (enrollments)
        students_m2m = course.students.all()
        
        # Get students through direct relationship (course_id in students table)
        students_direct = Student.query.filter_by(course_id=course.id).all()
        
        # Combine both lists and remove duplicates
        all_students = list(students_m2m)
        for student in students_direct:
            if student not in all_students:
                all_students.append(student)
        
        course_students[course] = all_students
    
    return render_template('lecturer/my_students.html', course_students=course_students, courses=courses) 