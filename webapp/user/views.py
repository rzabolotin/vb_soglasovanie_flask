from time import sleep

from flask import Blueprint, render_template, flash, redirect, url_for, session
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

    title = "ВБ удаленное согласование| Авторизация"
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/logout')
def logout():
    """Выход из профиля"""

    logout_user()
    flash('Вы успешно вышли из профиля')
    return redirect(url_for('user.login'))


def make_sleep_if_too_many_login_attempts():
    number_login_attempt = session.get('number_login_attempt', 0)

    number_login_attempt += 1

    session['number_login_attempt'] = number_login_attempt

    print(number_login_attempt)

    if number_login_attempt > 3:
        sleep(3)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    """Обработка формы авторизации"""
    make_sleep_if_too_many_login_attempts()

    form = LoginForm()
    user_name_lower = form.user_name.data.lower()
    if form.validate_on_submit():
        user = User.query.filter(User.user_name == user_name_lower).first()
        if user and user.password and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me)
            flash('Вы успешно вошли на сайт')
            session['number_login_attempt'] = 0
            return redirect(get_redirect_target())

    flash("Неправильные имя или пароль")
    return redirect(url_for('user.login'))

