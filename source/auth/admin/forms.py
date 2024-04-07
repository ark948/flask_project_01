from flask_wtf import FlaskForm
from wtforms import (
    StringField, EmailField, PasswordField, BooleanField, SubmitField
)

from wtforms.validators import (
    DataRequired
)

class AdminUserCreateForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired()])
    email = EmailField('ایمیل', validators=[DataRequired()])
    pwdhash = PasswordField('رمزعبور', validators=[DataRequired()])
    admin = BooleanField('دسترسی ادمین؟')
    submit = SubmitField('ثبت')

class AdminUserUpdateForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired()])
    email = EmailField('ایمیل', validators=[DataRequired()])
    admin = BooleanField('دسترسی ادمین؟')
    submit = SubmitField('ثبت')
    