from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, TelField, FileField
from wtforms.validators import DataRequired, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired()])
    email = EmailField('آدرس ایمیل', validators=[DataRequired()])
    password = PasswordField('رمزعبور', validators=[
        DataRequired(), 
        EqualTo('confirm', message='رمزعبور با تکرار آن همخوانی ندارد.')])
    confirm = PasswordField('تکرار رمزعبور', validators=[DataRequired()])
    submit = SubmitField('ثبت نام')

class LoginForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired()])
    password = PasswordField('رمزعبور', validators=[DataRequired()])
    remember_me = BooleanField('مرا بخاطر بسپار')
    submit = SubmitField('ورود')

class ResetPasswordRequestForm(FlaskForm):
    email = EmailField('آدرس ایمیل', validators=[DataRequired()])
    submit = SubmitField('درخواست تغییر رمزعبور')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('رمزعبور جدید', validators=[DataRequired()])
    confirm = PasswordField('تکرار رمز', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('ثبت')

class EmailVerificationRequestForm(FlaskForm):
    # email = EmailField('آدرس ایمیل', validators=[DataRequired()])
    submit = SubmitField('تایید')

class ProfileEditForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired()])
    email = EmailField('ایمیل', validators=[DataRequired()])
    phone_number = TelField('شماره تلفن')
    submit = SubmitField('ویرایش')

class ChangePasswordForm(FlaskForm):
    current = PasswordField('رمزعبور فعلی', validators=[DataRequired()])
    password = PasswordField('رمزعبور جدید', validators=[DataRequired()])
    confirm = PasswordField('تکرار رمزعبور جدید', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('ثبت')

class AvatarForm(FlaskForm):
    submit = SubmitField('بروزرسانی')