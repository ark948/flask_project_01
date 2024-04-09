from flask_wtf import FlaskForm
from wtforms import (
    StringField, EmailField, PasswordField, BooleanField, SubmitField
)

from wtforms.validators import (
    DataRequired
)

from flask_ckeditor import CKEditorField

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
    
class AdminUserCreateCKForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired()])
    email = EmailField('ایمیل', validators=[DataRequired()])
    pwdhash = PasswordField('رمزعبور', validators=[DataRequired()])
    admin = BooleanField('دسترسی ادمین؟')
    content = CKEditorField('Content')
    submit = SubmitField('ثبت')