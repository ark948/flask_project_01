from flask import render_template, url_for
from app.auth import bp

@bp.route('/')
def index():
    return render_template('auth/index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')