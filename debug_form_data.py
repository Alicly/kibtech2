from app import create_app, db
from app.forms.admin import CourseForm
from app.models.course import Course

app = create_app()

with app.app_context():
    # Test the form
    form = CourseForm()
    print("Form field type:", type(form.is_active))
    print("Form field data type:", type(form.is_active.data))
    print("Form field data:", form.is_active.data)
    
    # Test with a course object
    course = Course.query.first()
    if course:
        form_with_obj = CourseForm(obj=course)
        print("\nWith course object:")
        print("Form field data type:", type(form_with_obj.is_active.data))
        print("Form field data:", form_with_obj.is_active.data) 