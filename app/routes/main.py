from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from app.models import Course, ClassRoom, News, Event, Notification, SlideshowSlide
from app import db
from datetime import datetime, timedelta
from app.forms.contact import ContactForm
from flask_login import login_required, current_user
from app.models.system_setting import SystemSetting

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    # Get featured courses (first 3 active courses)
    featured_courses = Course.query.filter_by(is_active=True).limit(3).all()
    
    # Get latest news (first 3 published news)
    news = News.query.filter_by(is_published=True).order_by(News.date.desc()).limit(3).all()
    
    # Get upcoming events (first 3 events)
    events = Event.query.filter(Event.date >= datetime.now()).order_by(Event.date.asc()).limit(3).all()
    
    # Get active slideshow slides
    slideshow_slides = SlideshowSlide.get_active_slides()
    
    return render_template('main/index.html', 
                         featured_courses=featured_courses,
                         news=news,
                         events=events,
                         slideshow_slides=slideshow_slides)

@bp.route('/about')
def about():
    return render_template('main/about.html')

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Here you would typically send the email
        # For now, we'll just flash a success message
        flash('Thank you for your message. We will get back to you soon!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('main/contact.html', form=form)

@bp.route('/programs')
def programs():
    courses = Course.query.all()
    return render_template('main/programs.html', courses=courses)

@bp.route('/apply')
def apply():
    return render_template('main/apply.html')

@bp.route('/courses')
def courses():
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Number of courses per page
    
    # Get filter parameters
    category = request.args.get('category')
    level = request.args.get('level')
    
    # Start with base query
    query = Course.query
    
    # Apply filters if provided
    if category:
        query = query.filter_by(category=category)
    if level:
        query = query.filter_by(level=level)
    
    # Order by creation date (newest first)
    query = query.order_by(Course.created_at.desc())
    
    # Get paginated results
    courses = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('main/courses.html', courses=courses)

@bp.route('/course/<int:course_id>')
def course_details(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('main/course_details.html', course=course)

@bp.route('/gallery')
def gallery():
    return render_template('main/gallery.html')

@bp.route('/news')
def news():
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Number of news items per page
    
    # Get filter parameters
    category = request.args.get('category')
    date_filter = request.args.get('date')
    search_query = request.args.get('search', '').strip()
    
    # Start with base query
    query = News.query
    
    # Apply search if provided
    if search_query:
        query = query.filter(
            db.or_(
                News.title.ilike(f'%{search_query}%'),
                News.content.ilike(f'%{search_query}%')
            )
        )
    
    # Apply filters if provided
    if category:
        query = query.filter_by(category=category)
    if date_filter:
        today = datetime.now().date()
        if date_filter == 'today':
            query = query.filter(db.func.date(News.date) == today)
        elif date_filter == 'week':
            query = query.filter(db.func.date(News.date) >= today - timedelta(days=7))
        elif date_filter == 'month':
            query = query.filter(db.func.date(News.date) >= today - timedelta(days=30))
    
    # Order by date (newest first)
    query = query.order_by(News.date.desc())
    
    # Get paginated results
    news_list = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('main/news.html', 
                         news_list=news_list,
                         search_query=search_query,
                         category=category,
                         date_filter=date_filter)

@bp.route('/news/<int:news_id>')
def news_details(news_id):
    news_item = News.query.get_or_404(news_id)
    # Increment view count
    news_item.views += 1
    db.session.commit()
    return render_template('main/news_details.html', news=news_item)

@bp.route('/events')
def events():
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Number of events per page
    
    # Get filter parameters
    category = request.args.get('category')
    date_filter = request.args.get('date')
    search_query = request.args.get('search', '').strip()
    
    # Start with base query
    query = Event.query.filter(Event.date >= datetime.now()).order_by(Event.date.asc())
    
    # Apply search if provided
    if search_query:
        query = query.filter(
            db.or_(
                Event.title.ilike(f'%{search_query}%'),
                Event.description.ilike(f'%{search_query}%')
            )
        )
    
    # Apply filters if provided
    if category:
        query = query.filter_by(category=category)
    if date_filter:
        today = datetime.now().date()
        if date_filter == 'today':
            query = query.filter(db.func.date(Event.date) == today)
        elif date_filter == 'week':
            query = query.filter(db.func.date(Event.date) <= today + timedelta(days=7))
        elif date_filter == 'month':
            query = query.filter(db.func.date(Event.date) <= today + timedelta(days=30))
    
    # Get paginated results
    events_list = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('main/events.html', 
                         events_list=events_list,
                         search_query=search_query,
                         category=category,
                         date_filter=date_filter,
                         now=datetime.now())

@bp.route('/event/<int:event_id>')
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    # Get upcoming events (events after the current event date)
    upcoming_events = Event.query.filter(Event.date > event.date).order_by(Event.date.asc()).limit(3).all()
    return render_template('main/event_details.html', event=event, upcoming_events=upcoming_events)

@bp.route('/notifications')
@login_required
def notifications():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    notifications = Notification.query.filter_by(user_id=current_user.id)\
        .order_by(Notification.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('main/notifications.html', notifications=notifications)

@bp.route('/notifications/mark-read/<int:id>', methods=['POST'])
@login_required
def mark_notification_read(id):
    notification = Notification.query.get_or_404(id)
    if notification.user_id == current_user.id:
        notification.is_read = True
        db.session.commit()
    return redirect(url_for('main.notifications'))

@bp.route('/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False)\
        .update({'is_read': True})
    db.session.commit()
    return redirect(url_for('main.notifications')) 

@bp.context_processor
def inject_settings():
    """Inject system settings into all templates"""
    return {
        'config': {
            'INSTITUTE_LOGO': SystemSetting.get_setting('institute_logo'),
            'INSTITUTE_NAME': SystemSetting.get_setting('institute_name', 'KITELAKAPEL TECHNICAL TRAINING INSTITUTE'),
            'INSTITUTE_NAME_SHORT': SystemSetting.get_setting('institute_name', 'KITELAKAPEL').split()[0],
            'HERO_TITLE': SystemSetting.get_setting('hero_title', 'Empowering Kenya\'s Future Through Technical Education'),
            'HERO_SUBTITLE': SystemSetting.get_setting('hero_subtitle', 'Building a skilled workforce for Kenya\'s development through quality technical and vocational education.'),
            'HERO_BACKGROUND': SystemSetting.get_setting('hero_background'),
            'CAMPUS_IMAGE': SystemSetting.get_setting('campus_image'),
            'ABOUT_IMAGE': SystemSetting.get_setting('about_image'),
            'CONTACT_EMAIL': SystemSetting.get_setting('contact_email', 'info@kitelakapel.ac.ke'),
            'CONTACT_PHONE': SystemSetting.get_setting('contact_phone', '+254 700 000 000'),
            'CONTACT_ADDRESS': SystemSetting.get_setting('contact_address', 'Kitelakapel, Kenya')
        }
    } 

@bp.route('/test-slideshow')
def test_slideshow():
    slideshow_slides = SlideshowSlide.get_active_slides()
    return {
        'slides_count': len(slideshow_slides),
        'slides': [{'id': slide.id, 'title': slide.title, 'is_active': slide.is_active} for slide in slideshow_slides]
    } 