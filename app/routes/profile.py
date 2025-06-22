from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.forms.profile import ProfileForm

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def manage():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile.manage'))
    return render_template('profile/manage.html', form=form) 