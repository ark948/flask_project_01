from flask import (
    render_template, redirect, url_for, flash
)

from flask.views import (
    View
)

from flask_login import (
    current_user, login_required
)

from source.main import bp
from source.auth.admin.utils import admin_login_required

class IndexView(View):
    def dispatch_request(self):
        return render_template('main/index.html')


# route to test error handler
@bp.route('/er')
@login_required
@admin_login_required
def er():
    if current_user.is_authenticated and current_user.username == 'admin':
        raise Exception
    else:
        flash("این بخش برای تست سایت است.")
        return redirect(url_for('main.index'))
    
# registering class-based view
bp.add_url_rule('/', view_func=IndexView.as_view('index'))