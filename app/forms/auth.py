from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from app.models.user import User
from app.models.student import Student
from app.models.course import Course

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    role = SelectField('Role', choices=[
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('admin', 'Administrator'),
        ('staff', 'Staff')
    ], validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    # Common fields for all users
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=64)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=200)])
    role = SelectField('Role', choices=[
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('admin', 'Administrator'),
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
    lecturer_courses = SelectMultipleField('Courses Teaching', coerce=int, validators=[Optional()])
    
    # Staff specific fields
    staff_id = StringField('Staff ID', validators=[Optional(), Length(max=20)])
    position = StringField('Position', validators=[Optional(), Length(max=100)])
    
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Populate course choices
        self.course_id.choices = [(0, 'Select Course')] + [(c.id, f"{c.code} - {c.name}") for c in Course.query.filter_by(is_active=True).order_by(Course.name).all()]
        self.lecturer_courses.choices = [(c.id, f"{c.code} - {c.name}") for c in Course.query.filter_by(is_active=True).order_by(Course.name).all()]

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
    def validate_registration_number(self, registration_number):
        if self.role.data == 'student' and registration_number.data:
            student = Student.query.filter_by(student_number=registration_number.data).first()
            if student is not None:
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

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    new_password2 = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')

class UserSettingsForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[Optional()])
    submit = SubmitField('Save Changes') 