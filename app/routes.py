from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import db, login
from app.models import User, Course, Class, Assignment, Grade, Attendance, TeachingMaterial
from app.forms import LoginForm, RegistrationForm
from datetime import datetime
import json

# ... existing routes ...

# Note: Lecturer routes have been moved to app/routes/lecturer.py blueprint
# This file now only contains main application routes 