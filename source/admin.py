from flask_admin import (
    BaseView, expose, AdminIndexView
)

from flask_login import (
    current_user
)

from flask_admin.contrib.sqla import ModelView

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

class HelloView(BaseView):
    @expose('/')
    def index(self):
        return 'ok'

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()
    
class UserAdminView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()