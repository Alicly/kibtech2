from flask import Blueprint, render_template

bp = Blueprint('faq', __name__, url_prefix='/faq')

@bp.route('/')
def index():
    return render_template('faq/index.html') 