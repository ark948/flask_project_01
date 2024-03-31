from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from source.main import bp

@bp.route('/')
def index():
    return render_template('main/index.html')

# route to test error handler
@bp.route('/er')
def er():
    if current_user.is_authenticated and current_user.username == 'admin':
        raise Exception
    else:
        flash("این بخش برای تست سایت است.")
        return redirect(url_for('main.index'))