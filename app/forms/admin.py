from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, IntegerField, DateTimeField, FileField, SubmitField, DateField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, ValidationError
from app.models import Course, User, Student

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=200)])
    role = SelectField('Role', choices=[
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('admin', 'Admin'),
        ('staff', 'Staff')
    ], validators=[DataRequired()])
    
    # Student specific fields
    registration_number = StringField('Registration Number', validators=[Optional(), Length(max=20)])
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    gender = SelectField('Gender', choices=[
        ('', 'Select Gender'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], validators=[Optional()])
    course_id = SelectField('Course', coerce=int, validators=[Optional()])
    
    # Lecturer specific fields
    lecturer_id = StringField('Lecturer ID', validators=[Optional(), Length(max=20)])
    department = StringField('Department', validators=[Optional(), Length(max=100)])
    specialization = StringField('Specialization', validators=[Optional(), Length(max=100)])
    
    # Staff specific fields
    staff_id = StringField('Staff ID', validators=[Optional(), Length(max=20)])
    position = StringField('Position', validators=[Optional(), Length(max=100)])
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self._obj = kwargs.get('obj', None)
        self.course_id.choices = [(0, 'Select Course')] + [(c.id, f"{c.code} - {c.name}") for c in Course.query.filter_by(is_active=True).order_by(Course.name).all()]
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None and (not self._obj or user.id != self._obj.id):
            raise ValidationError('This email address is already registered. Please use a different email address.')
            
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None and (not self._obj or user.id != self._obj.id):
            raise ValidationError('This username is already taken. Please choose a different username.')
    
    def validate_registration_number(self, registration_number):
        if self.role.data == 'student' and registration_number.data:
            student = Student.query.filter_by(student_number=registration_number.data).first()
            # If editing, allow the current student's own registration number
            current_student = None
            if self._obj and hasattr(self._obj, 'email'):
                current_student = Student.query.filter_by(email=self._obj.email).first()
            if student is not None and (not current_student or student.id != current_student.id):
                raise ValidationError('This registration number is already registered.')
    
    def validate_lecturer_id(self, lecturer_id):
        if self.role.data == 'lecturer' and lecturer_id.data:
            user = User.query.filter_by(lecturer_id=lecturer_id.data).first()
            if user is not None:
                raise ValidationError('This lecturer ID is already registered.')
    
    def validate_staff_id(self, staff_id):
        if self.role.data == 'staff' and staff_id.data:
            user = User.query.filter_by(staff_id=staff_id.data).first()
            if user is not None:
                raise ValidationError('This staff ID is already registered.')

class CourseForm(FlaskForm):
    code = StringField('Course Code', validators=[DataRequired(), Length(max=20)])
    name = StringField('Course Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    duration = StringField('Duration', validators=[Optional(), Length(max=50)])
    level = StringField('Level', validators=[Optional(), Length(max=50)])
    category = StringField('Category', validators=[Optional(), Length(max=50)])
    capacity = IntegerField('Capacity', validators=[Optional(), NumberRange(min=1)])
    fee = FloatField('Course Fee (KES)', validators=[DataRequired(), NumberRange(min=0, message='Course fee must be a positive number')])
    entry_requirements = StringField('Entry Requirements', validators=[Optional(), Length(max=200)])
    exam_body = StringField('Examining Body', validators=[Optional(), Length(max=50)])
    lecturer_id = SelectField('Lecturer', coerce=int, validators=[Optional()])
    image = FileField('Course Image', validators=[Optional()])
    is_active = BooleanField('Active Course', validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self._obj = kwargs.get('obj', None)
        # Get all lecturers
        lecturers = User.query.filter_by(role='lecturer').all()
        self.lecturer_id.choices = [(0, 'Select Lecturer')] + [(l.id, f"{l.first_name} {l.last_name}") for l in lecturers]
        
    def validate_code(self, code):
        course = Course.query.filter_by(code=code.data).first()
        if course is not None and (not self._obj or course.id != self._obj.id):
            raise ValidationError('This course code is already taken. Please use a different code.')
    
    def validate_fee(self, fee):
        if fee.data and fee.data < 0:
            raise ValidationError('Course fee must be a positive number')

class ClassRoomForm(FlaskForm):
    name = StringField('Class Name', validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    lecturer_id = SelectField('Lecturer', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    day = SelectField('Day of Week', choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ], validators=[DataRequired()])
    start_time = StringField('Start Time', validators=[DataRequired()])
    end_time = StringField('End Time', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Save Class')
    
    def __init__(self, *args, **kwargs):
        super(ClassRoomForm, self).__init__(*args, **kwargs)
        self.course_id.choices = [(c.id, c.name) for c in Course.query.order_by(Course.name).all()]
        self.lecturer_id.choices = [(0, 'Select Lecturer')] + [
            (t.id, f"{t.first_name} {t.last_name}") 
            for t in User.query.filter_by(role='lecturer').order_by(User.first_name).all()
        ]

class NewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('announcement', 'Announcement'),
        ('event', 'Event'),
        ('achievement', 'Achievement'),
        ('general', 'General')
    ], validators=[DataRequired()])
    image = FileField('Image', validators=[Optional()])

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    event_date = DateTimeField('Event Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    image = FileField('Image', validators=[Optional()])
    submit = SubmitField('Save Event') 

class MaintenanceModeForm(FlaskForm):
    maintenance_mode = SelectField('Maintenance Mode', choices=[('off', 'Off'), ('on', 'On')], validators=[DataRequired()])
    submit = SubmitField('Update') 

class HomepageSettingsForm(FlaskForm):
    institute_logo = FileField('Institute Logo', validators=[Optional()])
    hero_background = FileField('Hero Background Image', validators=[Optional()])
    campus_image = FileField('Campus Image', validators=[Optional()])
    about_image = FileField('About Section Image', validators=[Optional()])
    hero_title = StringField('Hero Title', validators=[DataRequired()])
    hero_subtitle = TextAreaField('Hero Subtitle', validators=[DataRequired()])
    institute_name = StringField('Institute Name', validators=[DataRequired()])
    institute_tagline = StringField('Institute Tagline', validators=[Optional()])
    contact_email = StringField('Contact Email', validators=[Optional(), Email()])
    contact_phone = StringField('Contact Phone', validators=[Optional()])
    contact_address = TextAreaField('Contact Address', validators=[Optional()])
    submit = SubmitField('Save Settings') 

class UnitForm(FlaskForm):
    code = StringField('Unit Code', validators=[DataRequired(), Length(max=20)])
    name = StringField('Unit Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    credits = IntegerField('Credits', validators=[Optional(), NumberRange(min=0)])
    course_id = IntegerField('Course ID', validators=[DataRequired()])  # Hidden or pre-filled in the form
    submit = SubmitField('Save Unit') 

class SlideshowSlideForm(FlaskForm):
    title = StringField('Slide Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Slide Description', validators=[DataRequired()])
    image = FileField('Slide Image', validators=[DataRequired()])
    order = IntegerField('Display Order', validators=[Optional(), NumberRange(min=0)])
    is_active = BooleanField('Active Slide', default=True)
    submit = SubmitField('Save Slide')

class SlideshowSlideEditForm(FlaskForm):
    title = StringField('Slide Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Slide Description', validators=[DataRequired()])
    image = FileField('Slide Image', validators=[Optional()])
    order = IntegerField('Display Order', validators=[Optional(), NumberRange(min=0)])
    is_active = BooleanField('Active Slide', default=True)
    submit = SubmitField('Update Slide') 