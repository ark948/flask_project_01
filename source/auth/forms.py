from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired()])
    email = EmailField('آدرس ایمیل', validators=[DataRequired()])
    password = PasswordField('رمزعبور', validators=[DataRequired(), EqualTo('confirm')])
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