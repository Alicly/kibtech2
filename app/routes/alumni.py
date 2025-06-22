from flask import Blueprint, render_template
from app.models.alumni import Alumni

bp = Blueprint('alumni', __name__, url_prefix='/alumni')
 
@bp.route('/')
def index():
    alumni = Alumni.query.filter_by(is_published=True).all()
    return render_template('alumni/index.html', alumni=alumni) 