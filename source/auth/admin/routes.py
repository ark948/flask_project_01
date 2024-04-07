from source import db

from source.auth.admin import bp

from flask_login import (
    login_required, current_user
)

from source.models.user import (
    User
)

from flask import (
    render_template, flash, redirect, url_for
)

from source.auth.admin.forms import (
    AdminUserCreateForm, AdminUserUpdateForm
)

from source.auth.admin.utils import (
    admin_login_required, insert_user_admin
)

from icecream import ic
ic.configureOutput(includeContext=True)

@bp.route('/')
@login_required
@admin_login_required
def index():
    return render_template('auth/admin/index.html')

@bp.route('/users-list')
@login_required
@admin_login_required
def users_list_admin():
    users = User.query.all()
    return render_template('auth/admin/users_list_admin.html', users=users)

@bp.route('/create-user', methods=['GET', 'POST'])
@login_required
@admin_login_required
def user_create_admin():
    form = AdminUserCreateForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.pwdhash.data
        admin = form.admin.data
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash("نام کاربری قبلا ثبت شده است.", 'danger') # to be changed to warning later
            return redirect(url_for('auth.admin.user_create_admin'))
        try:
            response = insert_user_admin(username, email, password, admin)
            if response['result'] == True:
                flash('کاربر با موفقیت افزورده شد.', 'success')
                return redirect(url_for('auth.admin.user_create_admin'))
            else:
                flash("خطا در فرایند افزودن.", 'danger')
                ic(response['message'])
                return redirect(url_for('auth.admin.user_create_admin'))
        except Exception as new_user_admin_error:
            ic(new_user_admin_error)
            flash("خطا در فرایند افزودن کاربر جدید.", 'danger')
            return redirect(url_for('auth.admin.user_create_admin'))
    
    if form.errors:
        ic(form.errors)
        flash("خطا در فرم", 'danger')
        return redirect(url_for('auth.admin.user_create_admin.'))
        # flash(form.errors, 'danger')
    return render_template('auth/admin/user_create_admin.html', form=form)

@bp.route('/update-user/<id>', methods=['GET', 'POST'])
@login_required
@admin_login_required
def user_update_admin(id):
    user = User.query.get(id)
    form = AdminUserUpdateForm(
        username=user.username,
        email=user.email,
        admin=user.admin
    )

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        admin = form.admin.data

        try:
            User.query.filter_by(id=id).update({
                    'username': username,
                    'email': email,
                    'admin': admin
                })
        except Exception as update_error_by_query:
            ic(update_error_by_query)
            flash("خطا در فرایند ویرایش", 'danger')
            return redirect(url_for('auth.admin.users_list_admin'))
        
        try:
            db.session.commit()
            flash("بروزرسانی کاربر با موفقیت انجام شد.", 'success')
            return redirect(url_for('auth.admin.users_list_admin'))
        except Exception as update_commit_error:
            ic(update_commit_error)
            flash("خطا در ثبت ویرایش.", 'danger')
            return redirect(url_for('auth.admin.users_list_admin'))
    if form.errors:
        ic(form.errors)
        # flash(form.errors, 'danger')
        flash("خطا در فرم", 'danger')
        return redirect(url_for('auth.admin.users_list_admin'))

    return render_template('auth/admin/user_update_admin.html', form=form, user=user)

@bp.route('/delete-user/<id>', methods=['POST'])
@login_required
@admin_login_required
def user_delete_admin(id):
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        flash("کاربر با موفقیت حذف شد.", 'success')
        return redirect(url_for('auth.admin.users_list_admin'))
    except Exception as user_delete_error:
        ic(user_delete_error)
        flash("خطا در فرایند حذف", 'danger')
        return redirect(url_for('auth.admin.users_list_admin'))