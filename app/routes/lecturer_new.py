from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import ClassRoom, Assignment, Grade, Attendance
from app import db
from datetime import datetime

bp = Blueprint('lecturer', __name__)

@bp.before_request
def before_request():
    if not current_user.is_authenticated or current_user.role != 'lecturer':
        flash('You must be logged in as a lecturer to access this page.', 'error')
        return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get today's schedule
    today = datetime.now().strftime('%A')
    today_schedule = ClassRoom.query.filter_by(
        lecturer_id=current_user.id,
        day=today
    ).order_by(ClassRoom.start_time).all()
    
    # Get recent activities
    recent_activities = get_recent_activities()
    
    return render_template('lecturer/dashboard.html',
                         today_schedule=today_schedule,
                         recent_activities=recent_activities)

def get_recent_activities():
    # Get recent grades
    recent_grades = Grade.query.join(Assignment)\
        .filter(Assignment.lecturer_id == current_user.id)\
        .order_by(Grade.submitted_at.desc()).limit(5).all()
    
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