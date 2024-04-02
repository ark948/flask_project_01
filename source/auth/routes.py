from flask import (
    render_template, url_for, flash, request, redirect, current_app
)
from source.auth import bp
from source.auth.forms import (
    RegisterForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm, EmailVerificationRequestForm
)
from source import db, Captcha
from flask_login import (
    login_user, logout_user, current_user, login_required
)
from source.models.user import User
from icecream import ic
ic.configureOutput(includeContext=True)
from sqlalchemy import select
from source.email import (
    send_password_reset_email, send_email_verification_email
)
import datetime
import convertdate

# jinja custom filter
@bp.add_app_template_filter
def to_persian(dt):
    return convertdate.persian.from_gregorian(int(dt.strftime("%Y")), int(dt.strftime("%m")), int(dt.strftime("%d")))

@bp.route('/')
def index():
    if current_user.is_authenticated:
        flash("این صفحه برای کاربرانی که وارد سایت شده اند، مجاز نیست.")
        return redirect(url_for('main.index'))
    return render_template('auth/index.html')

def insert_user_object(username, email, password, confirm):
    try:
        new_user_object = User(username, email)
    except Exception as user_creation_error:
        ic(user_creation_error)
        return False
    if password == confirm:
        try:
            new_user_object.set_password(password)
            db.session.add(new_user_object)
            db.session.commit()
            return True
        except Exception as user_insertion_error:
            ic(user_insertion_error)
            return False
    else:
        return False

# no link to this route
# old register route deleted (no support for testing - captcha)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if current_app.config['TESTING'] == True:
        form = RegisterForm()
        if form.validate_on_submit():
            result = insert_user_object(form.username.data, form.email.data, form.password.data, form.confirm.data)
            if result == True:
                return redirect(url_for('auth.login'))
            elif result == False:
                return redirect(url_for('auth.register'))
        return render_template('auth/register.html', form=form)
    elif current_app.config['TESTING'] == False or current_app.config['TESTING'] == None:
        form = RegisterForm()
        new_captcha_dict = Captcha.create()
        if form.validate_on_submit():
            c_hash = request.form['captcha-hash']
            c_text = request.form['captcha-text']
            if Captcha.verify(c_text, c_hash):
                result = insert_user_object(form.username.data, form.email.data, form.password.data, form.confirm.data)
                if result == True:
                    flash("ثبت نام با موفقیت انجام شد.")
                    return redirect(url_for('auth.login'))
                elif result == False:
                    flash("خطا در فرایند ثبت نام.")
                    return redirect(url_for('auth.register'))
            else:
                flash("کد امنیتی اشتباه وارد شده است.")
                return redirect(url_for('auth.register'))
        return render_template('auth/register.html', form=form, captcha=new_captcha_dict)

# old login route removed (no support for testing - captcha)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("شما وارد سایت شده اید.")
        return redirect(url_for('main.index'))
    if current_app.config['TESTING'] == True:
        form = LoginForm()
        try:
            user = db.session.scalar(select(User).where(User.username==form.username.data))
            if user is None or user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('main.index'))
        except Exception as login_error_testing:
            flash("Error")
            return redirect(url_for('auth.login'))
        return render_template('auth/login.html', form=form)
    elif current_app.config['TESTING'] == False or current_app.config['TESTING'] == None:
        new_captcha_dict = Captcha.create()
        form = LoginForm()
        if form.validate_on_submit():
            c_hash = request.form['captcha-hash']
            c_text = request.form['captcha-text']
            if Captcha.verify(c_text, c_hash):
                try:
                    user = db.session.scalar(select(User).where(User.username==form.username.data))
                    if user is None or not user.check_password(form.password.data):
                        flash("نام کاربری و یا پسورد اشتباه است.")
                        return redirect(url_for('auth.login'))
                    login_user(user, remember=form.remember_me.data)
                    flash("با موفقیت وارد سایت شدید.")
                    return redirect(url_for('main.index'))
                except Exception as login_error:
                    ic(login_error)
                    flash("خطا در فرآیند ورود.")
                    return redirect(url_for('auth.login'))
        return render_template('auth/login.html', form=form, captcha=new_captcha_dict)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('auth/profile.html')

@bp.route('/email-verification-request', methods=['GET', 'POST'])
@login_required
def email_verification_request():
    if current_user.is_verified == True:
        flash("ایمیل شما قبلا تایید شده است.")
        return redirect(url_for('auth.profile'))
    form = EmailVerificationRequestForm()
    if form.validate_on_submit():
        send_email_verification_email(current_user)
    return render_template('auth/ev_request.html', form=form)

@bp.route('/verify-email/<token>', methods=['GET', 'POST'])
@login_required
def verify_email(token):
    if current_user.is_verified == True:
        flash("ایمیل شما قبلا تایید شده است.")
        return redirect(url_for('auth.profile'))
    result = None
    try:
        result = User.verify_email_verification_token(token)
        ic(result)
    except Exception as tok_ver_er:
        ic(tok_ver_er)
        flash("خطا در فرایند تایید، لطفا دوباره تلاش کنید.")
        return redirect(url_for('main.index'))
    if result == True:
        try:
            user_object = User.query.get(current_user.id)
            user_object.is_verified = True
            user_object.verified_on = datetime.datetime.now()
            db.session.commit()
            flash("ایمیل شما با موفقیت تایید شد.")
            return redirect(url_for('main.index'))
        except Exception as user_ver_er:
            ic(user_ver_er)
            flash('خطا در فرایند تایید')
            return redirect(url_for('main.index'))
    else:
        flash("خطا در فرایند تایید. لطفا دوباره تلاش کنید.")
        return redirect(url_for('main.index'))

        
@bp.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        flash("شما وارد سایت شده اید. درصورت فراموشی رمز، از سایت خارج شده و سپس  برای بازیابی اقدام کنید.")
        return redirect(url_for('auth.index'))
    form = ResetPasswordRequestForm()
    new_captcha_dict = Captcha.create()
    if form.validate_on_submit():
        c_hash = request.form['captcha-hash']
        c_text = request.form['captcha-text']
        if Captcha.verify(c_text, c_hash):
            user = db.session.scalar(
                select(User).where(User.email==form.email.data)
            )
            if user:
                send_password_reset_email(user)
                flash("یک ایمیل حاوی لینک بازیابی برای شما ارسال شد.")
                return redirect(url_for('auth.index'))
            else:
                flash("خطا امنیتی")
                return redirect(url_for('auth.index'))
        else:
            flash("کد امنیتی اشتباه وارد شده است.")
            return redirect(url_for('auth.index'))
    return render_template('auth/reset_password_request.html', form=form, captcha=new_captcha_dict)

@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        flash("لطفا خارج شوید.")
        return redirect(url_for('auth.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        # if user was not found
        flash("خطا داخلی")
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('رمزعبور شما با موفقیت تغییر کرد.')
        return redirect(url_for('auth.index'))
    return render_template('auth/reset_password.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("کابر با موقیت خارج شد.")
    return redirect(url_for('main.index'))