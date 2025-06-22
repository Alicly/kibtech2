from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    email = EmailField('Email Address', validators=[
        DataRequired(),
        Email()
    ])
    subject = StringField('Subject', validators=[
        DataRequired(),
        Length(min=2, max=200)
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=10, max=1000)
    ])
    submit = SubmitField('Send Message') 