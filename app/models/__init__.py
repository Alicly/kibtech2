from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db

# Import models in order of dependencies
from app.models.user import User
from app.models.course import Course
from app.models.class_room import ClassRoom
from app.models.assignment import Assignment
from app.models.grade import Grade
from app.models.attendance import Attendance
from app.models.teaching_material import TeachingMaterial
from app.models.workshop import Workshop
from app.models.tool import Tool
from app.models.enrollment import Enrollment
from app.models.news import News
from app.models.event import Event
from app.models.notification import Notification
from app.models.module import Module
from app.models.unit_registration import UnitRegistration
from app.models.unit import Unit
from app.models.fee_structure import FeeStructure
from app.models.payment import Payment
from app.models.class_schedule import ClassSchedule
from app.models.leadership import LeadershipTeam
# from app.models.maintenance import MaintenanceRecord, MaintenanceRequest  # Temporarily disabled
from app.models.assessment import Assessment, AssessmentSubmission
from app.models.exam import Exam, ExamResult
from app.models.student import Student
from app.models.fee import Fee
from app.models.assignment_submission import AssignmentSubmission
# from app.models.lesson import Lesson  # Removed because lesson.py does not exist
# from app.models.quiz import Quiz  # Removed because quiz.py does not exist
# from app.models.question import Question  # Removed because question.py does not exist
# from app.models.answer import Answer  # Removed because answer.py does not exist
# from app.models.student_progress import StudentProgress  # Removed because student_progress.py does not exist
# from app.models.feedback import Feedback  # Removed because feedback.py does not exist
# from app.models.certificate import Certificate  # Removed because certificate.py does not exist
# from app.models.audit_log import AuditLog  # Removed because audit_log.py does not exist
# from app.models.fee_model import FeePayment  # Removed because fee_model.py does not exist
# from app.models.exam_model import Exam, ExamResult  # Removed because exam_model.py does not exist
# from app.models.leadership import LeadershipTeam  # Removed because leadership.py does not exist
# from app.models.fee_model import FeePayment  # Removed because fee_model.py does not exist
# from app.models.booking import Booking  # Removed because booking.py does not exist
# from app.models.report import Report  # Removed because report.py does not exist
# from app.models.maintenance import MaintenanceRecord, ToolUsage  # Temporarily disabled to fix initialization
# from app.models.audit_log import AuditLog  # Removed because audit_log.py does not exist
# from app.models.fee_model import FeePayment  # Removed because fee_model.py does not exist
# from app.models.exam_model import Exam, ExamResult  # Removed because exam_model.py does not exist
# from app.models.leadership import LeadershipTeam  # Removed because leadership.py does not exist
from app.models.announcement import Announcement
from app.models.slideshow import SlideshowSlide

# Note: User loader is defined in user.py, no need to duplicate here

__all__ = [
    'User',
    'Course',
    'ClassRoom',
    'Unit',
    'Student',
    'UnitRegistration',
    'Grade',
    'Fee',
    'FeeStructure',
    'Payment',
    'Assignment',
    'AssignmentSubmission',
    'Attendance',
    'ClassSchedule',
    'News',
    'Event',
    'Notification',
    'LeadershipTeam',
    # 'MaintenanceRecord',  # Temporarily disabled
    # 'MaintenanceRequest',  # Temporarily disabled
    'Assessment',
    'AssessmentSubmission',
    'Exam',
    'ExamResult',
    'TeachingMaterial',
    'Announcement',
    'SlideshowSlide'
] 