# TVET Management System - Heroku Deployment Guide

## 🚀 Quick Deployment

### Prerequisites
1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure git is installed and configured

### Step-by-Step Deployment

#### 1. Prepare Your Application
```bash
# Clone or navigate to your project directory
cd TVET1

# Ensure all files are committed to git
git add .
git commit -m "Prepare for Heroku deployment"
```

#### 2. Create Heroku App
```bash
# Login to Heroku
heroku login

# Create a new app (replace 'your-app-name' with your desired name)
heroku create your-app-name

# Or let Heroku generate a name
heroku create
```

#### 3. Add PostgreSQL Database
```bash
# Add PostgreSQL addon (free tier)
heroku addons:create heroku-postgresql:mini

# Verify database URL is set
heroku config:get DATABASE_URL
```

#### 4. Set Environment Variables
```bash
# Set secret key
heroku config:set SECRET_KEY="your-secret-key-here"

# Set Flask environment
heroku config:set FLASK_ENV=production
heroku config:set FLASK_APP=app.py
```

#### 5. Deploy Application
```bash
# Deploy to Heroku
git push heroku main

# If you're on master branch
git push heroku master
```

#### 6. Run Database Migrations
```bash
# Run migrations
heroku run flask db upgrade
```

#### 7. Create Admin User
```bash
# Create admin user
heroku run python create_test_users.py
```

#### 8. Open Your Application
```bash
# Open in browser
heroku open
```

## 🔧 Configuration Details

### Environment Variables
Set these in Heroku dashboard or via CLI:

```bash
# Required
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
FLASK_APP=app.py

# Optional (for email functionality)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Database Configuration
The application automatically detects and uses the `DATABASE_URL` environment variable provided by Heroku PostgreSQL.

## 📊 Application Features

### Default Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@tvet.ac.ke`

### User Roles
1. **Admin**: Full system access
2. **Lecturer**: Course and student management
3. **Staff**: Administrative tasks
4. **Student**: Course enrollment and grades

## 🛠️ Maintenance Commands

### View Logs
```bash
# View recent logs
heroku logs

# Follow logs in real-time
heroku logs --tail
```

### Database Operations
```bash
# Run migrations
heroku run flask db upgrade

# Create new migration
heroku run flask db migrate -m "Description"

# Reset database (WARNING: This will delete all data)
heroku run flask db downgrade base
heroku run flask db upgrade
```

### Shell Access
```bash
# Open Python shell
heroku run flask shell

# Run custom scripts
heroku run python your_script.py
```

### Restart Application
```bash
# Restart dynos
heroku restart
```

## 🔒 Security Considerations

### Change Default Passwords
1. Login as admin
2. Go to Profile settings
3. Change admin password
4. Update other user passwords

### Environment Variables
- Never commit sensitive data to git
- Use Heroku config vars for secrets
- Regularly rotate SECRET_KEY

### Database Security
- PostgreSQL is automatically secured by Heroku
- Regular backups are recommended
- Monitor database usage

## 📈 Scaling (Optional)

### Upgrade Database
```bash
# Upgrade to paid PostgreSQL plan
heroku addons:upgrade heroku-postgresql:mini heroku-postgresql:basic
```

### Add Dynos
```bash
# Scale web dynos
heroku ps:scale web=2
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Build Fails
```bash
# Check build logs
heroku logs --tail

# Common fixes:
# - Ensure all dependencies are in requirements.txt
# - Check Python version in runtime.txt
# - Verify Procfile exists and is correct
```

#### 2. Database Connection Issues
```bash
# Check database URL
heroku config:get DATABASE_URL

# Test database connection
heroku run flask shell
# Then in shell: from app import db; db.engine.execute('SELECT 1')
```

#### 3. Application Errors
```bash
# Check application logs
heroku logs --tail

# Restart application
heroku restart
```

#### 4. Migration Issues
```bash
# Check migration status
heroku run flask db current

# Reset migrations if needed
heroku run flask db stamp head
```

## 📞 Support

### Heroku Support
- [Heroku Documentation](https://devcenter.heroku.com/)
- [Heroku Status](https://status.heroku.com/)
- [Heroku Support](https://help.heroku.com/)

### Application Support
- Check logs: `heroku logs --tail`
- Review error messages in application
- Verify environment variables are set correctly

## 🎯 Next Steps

After successful deployment:

1. **Test all features**:
   - User registration and login
   - Course management
   - Student enrollment
   - Grade management
   - File uploads

2. **Configure email** (if needed):
   - Set up SMTP settings
   - Test email functionality

3. **Add content**:
   - Create courses
   - Add students and lecturers
   - Upload materials

4. **Monitor performance**:
   - Check Heroku metrics
   - Monitor database usage
   - Review application logs

5. **Set up backups**:
   - Configure database backups
   - Set up monitoring alerts

## 🏆 Success!

Your TVET Management System is now live on Heroku! 

**Application URL**: `https://your-app-name.herokuapp.com`

Remember to:
- Change default passwords
- Add your institution's branding
- Configure email settings
- Set up regular backups
- Monitor application performance

Happy teaching! 🎓 