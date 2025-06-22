# TVET Management System

A comprehensive Technical and Vocational Education and Training (TVET) management system built with Flask. This system provides complete management capabilities for educational institutions including student management, course administration, grading, attendance tracking, and more.

## 🚀 Features

### User Management
- **Multi-role System**: Admin, Lecturer, Staff, Student
- **Dynamic Registration**: Role-specific registration forms
- **Profile Management**: User profile updates and management
- **Authentication**: Secure login/logout system

### Course Management
- **Course Creation**: Add and manage courses with fees
- **Course Details**: Comprehensive course information
- **Enrollment**: Student course enrollment system
- **Fee Management**: Course fee tracking and management

### Academic Management
- **Assignment Management**: Create and manage assignments
- **Grading System**: Comprehensive grading and feedback
- **Attendance Tracking**: Student attendance monitoring
- **Exam Management**: Exam scheduling and results

### Administrative Features
- **Dashboard**: Role-specific dashboards
- **Reports**: Academic and administrative reports
- **Notifications**: System-wide notifications
- **Activity Logs**: User activity tracking

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL (Heroku) / SQLite (Development)
- **ORM**: SQLAlchemy with Flask-Migrate
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Deployment**: Heroku

## 📋 Prerequisites

- Python 3.10+
- Git
- Heroku CLI (for deployment)
- PostgreSQL (for production)

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TVET1
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "SECRET_KEY=your-secret-key-here" > .env
   echo "FLASK_APP=app.py" >> .env
   echo "FLASK_ENV=development" >> .env
   ```

5. **Initialize database**
   ```bash
   flask db upgrade
   python create_test_users.py
   ```

6. **Run the application**
   ```bash
   flask run
   ```

7. **Access the application**
   - Open http://localhost:5000
   - Login with admin/admin123

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

4. **Add PostgreSQL database**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY="your-secret-key-here"
   heroku config:set FLASK_ENV=production
   heroku config:set FLASK_APP=app.py
   ```

6. **Deploy to Heroku**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

7. **Run database migrations**
   ```bash
   heroku run flask db upgrade
   ```

8. **Create admin user**
   ```bash
   heroku run python create_test_users.py
   ```

9. **Open the application**
   ```bash
   heroku open
   ```

## 👥 User Roles and Access

### Admin
- **Username**: `admin`
- **Password**: `admin123`
- **Access**: Full system administration

### Lecturer
- **Username**: `lecturer1`
- **Password**: `password123`
- **Access**: Course management, grading, attendance

### Staff
- **Username**: `staff1`
- **Password**: `password123`
- **Access**: Administrative tasks, student management

### Student
- **Username**: `student1`
- **Password**: `password123`
- **Access**: Course enrollment, grades, assignments

## 📁 Project Structure

```
TVET1/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models/              # Database models
│   ├── routes/              # Application routes
│   ├── forms/               # WTForms
│   ├── static/              # Static files (CSS, JS, images)
│   ├── templates/           # HTML templates
│   └── utils/               # Utility functions
├── migrations/              # Database migrations
├── config.py               # Configuration settings
├── app.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── Procfile               # Heroku deployment
├── runtime.txt            # Python version
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `you-will-never-guess` |
| `DATABASE_URL` | Database connection URL | SQLite local file |
| `FLASK_ENV` | Flask environment | `development` |
| `FLASK_APP` | Flask application | `app.py` |

### Database Configuration

The application automatically detects the database URL:
- **Development**: Uses SQLite database
- **Production**: Uses PostgreSQL (Heroku)

## 🗄️ Database Management

### Local Development
```bash
# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

### Heroku Production
```bash
# Run migrations
heroku run flask db upgrade

# Create migration
heroku run flask db migrate -m "Description"
```

## 🔒 Security Features

- **Password Hashing**: Secure password storage
- **Session Management**: Secure session handling
- **CSRF Protection**: Cross-site request forgery protection
- **Input Validation**: Form validation and sanitization
- **Role-based Access**: Role-specific permissions

## 📊 Features by Role

### Admin Dashboard
- User management
- Course management
- System settings
- Reports and analytics
- Activity logs

### Lecturer Dashboard
- Course management
- Assignment creation
- Grade management
- Attendance tracking
- Student progress

### Staff Dashboard
- Student management
- Administrative tasks
- Resource management
- Communication tools

### Student Dashboard
- Course enrollment
- Assignment submission
- Grade viewing
- Attendance tracking
- Fee management

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check database URL
   heroku config:get DATABASE_URL
   
   # Test connection
   heroku run flask shell
   ```

2. **Migration Issues**
   ```bash
   # Check migration status
   heroku run flask db current
   
   # Reset migrations
   heroku run flask db stamp head
   ```

3. **Build Failures**
   ```bash
   # Check build logs
   heroku logs --tail
   
   # Verify requirements.txt
   pip freeze > requirements.txt
   ```

### Logs and Debugging

```bash
# View application logs
heroku logs --tail

# Run shell for debugging
heroku run flask shell

# Check environment variables
heroku config
```

## 📈 Performance Optimization

- **Database Indexing**: Optimized database queries
- **Static File Caching**: Efficient static file serving
- **Lazy Loading**: Optimized model relationships
- **Connection Pooling**: Database connection optimization

## 🔄 Updates and Maintenance

### Regular Maintenance
1. **Database Backups**: Regular PostgreSQL backups
2. **Security Updates**: Keep dependencies updated
3. **Performance Monitoring**: Monitor application metrics
4. **Log Analysis**: Regular log review

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Run migrations
flask db upgrade

# Deploy to Heroku
git push heroku main
```

## 📞 Support

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

### Issues and Bugs
- Check application logs: `heroku logs --tail`
- Review error messages in the application
- Verify environment variables are set correctly

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🎯 Roadmap

- [ ] Email notifications
- [ ] Mobile app support
- [ ] Advanced reporting
- [ ] API endpoints
- [ ] Multi-language support
- [ ] Advanced analytics

---

**Happy Teaching! 🎓**

For more information, visit the [deployment guide](heroku_deployment_guide.md). 