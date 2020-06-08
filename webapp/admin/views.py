from flask import abort
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import PasswordField

from webapp.user.models import User

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class MyUserView(ModelView):
    form_excluded_columns = ('password')
    #  Form will now use all the other fields in the model

    #  Add our own password form field - call it password2
    form_extra_fields = {
        'password2': PasswordField('Password')
    }

    # set the form fields to use
    form_columns = (
        'id',
        'username',
        'email',
        'role',
        'password2',
     )

    def on_model_change(self, form, User, is_created):
        if form.password2.data is not None:
            User.set_password(form.password2.data)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if (not current_user.is_authenticated 
            or not current_user.is_admin):
            return abort(403)
        return super(MyAdminIndexView, self).index()