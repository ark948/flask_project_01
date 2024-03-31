from flask import render_template, url_for, flash, request, redirect, current_app
from source.auth import bp
from source.auth.forms import RegisterForm, LoginForm
from source import db, Captcha, login_manager
from flask_login import login_user, logout_user, current_user, login_required
from source.models.user import User
from icecream import ic
from sqlalchemy import select

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
@bp.route('/old-register', methods=['GET', 'POST'])
def old_register():
    if current_user.is_authenticated:
        flash("شما قبلا در سایت ثبت نام کرده اید.")
        return redirect(url_for('main.index'))
    form = RegisterForm()
    new_captcha_dict = Captcha.create()
    if form.validate_on_submit():
        c_hash = request.form['captcha-hash']
        c_text = request.form['captcha-text']
        if Captcha.verify(c_text, c_hash):
            try:
                new_user_object = User(form.username.data, form.email.data)
                if form.password.data == form.confirm.data:
                    new_user_object.set_password(form.password.data)
                    try:
                        db.session.add(new_user_object)
                        db.session.commit()
                        flash("ثبت نام با موفقیت انجام شد. می توانید وارد سایت شوید.")
                        return redirect(url_for('auth.login'))
                    except Exception as db_error:
                        # database commit error
                        ic(db_error)
                        flash("خطا پایگاه داده. لطفا نام کاربری و ایمیل دیگری وارد کنید.")
                        return redirect(url_for('auth.register'))
            except Exception as register_error:
                # User model and password process error
                ic(register_error)
                flash("خطای سیستم. لطفا لحظاتی بعد مجدد تلاش کرده و یا با ")
        else:
            # captcha error
            print("Captcha Failed")
            flash("کد امنیتی اشتباه وارد شده است. دوباره تلاش کنید.")
            return redirect(url_for('auth.register'))
    return render_template('auth/old_register.html', form=form, captcha=new_captcha_dict)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("شما قبلا در سایت ثبت نام کرده اید.")
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if current_app.config['TESTING'] == True:
        form = RegisterForm()
        if form.validate_on_submit():
            result = insert_user_object(form.username.data, form.email.data, form.password.data, form.confirm.data)
            if result == True:
                flash("ثبت نام با موفقیت انجام شد.")
                return redirect(url_for('auth.login'))
            elif result == False:
                flash("خطا در فرایند ثبت نام.")
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

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("شما وارد سایت شده اید.")
        return redirect(url_for('main.index'))
    new_captcha_dict = Captcha.create()
    form = LoginForm()
    if form.validate_on_submit():
        c_hash = request.form['captcha-hash']
        c_text = request.form['captcha-text']
        if Captcha.verify(c_text, c_hash):
            try:
                user = db.session.scalar(select(User).where(User.username==form.username.data))
                if user is None or not user.check_password(form.password.data):
                    # if user did not exist or check_password returned false
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

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("کابر با موقیت خارج شد.")
    return redirect(url_for('main.index'))