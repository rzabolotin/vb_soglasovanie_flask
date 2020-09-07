from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from webapp.user.forms import LoginForm
from webapp.user.models import User
from webapp.utils import get_redirect_target


blueprint = Blueprint('user', __name__, url_prefix='/users/')


@blueprint.route('/login')
def login():
    """Форма авторизации"""

    if current_user.is_authenticated:
        return redirect(get_redirect_target())

    title = "Авторизация"
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/logout')
def logout():
    """Выход из профиля"""

    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('user.login'))


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    """Обработка формы авторизации"""

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.user_name == form.user_name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me)
            flash('Вы успешно вошли на сайт')
            return redirect(get_redirect_target())

    flash("Неправильные имя или пароль")
    return redirect(url_for('user.login'))

