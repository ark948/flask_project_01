from flask import render_template, url_for, flash, request, redirect
from app.auth import bp
from app.auth.forms import RegisterForm
from app import Captcha

@bp.route('/')
def index():
    return render_template('auth/index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    new_captcha_dict = Captcha.create()
    if form.validate_on_submit():
        c_hash = request.form['captcha-hash']
        c_text = request.form['captcha-text']
        if Captcha.verify(c_text, c_hash):
            try:
                print("OK")
            except Exception as register_error:
                print("NOT OK")
        else:
            print("Captcha Failed")
            flash("Incorrect Captcha")
            return redirect(url_for('auth.register'))
    return render_template('auth/register.html', form=form, captcha=new_captcha_dict)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')