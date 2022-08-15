from flask import Flask, render_template
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate

from webapp.admin.views import MyAdminIndexView, MyBusinessProcessView, MyModelView, MyUserView
from webapp.api.views import blueprint as api_blueprint
from webapp.filters import register_my_jinja_filters
from webapp.model import db, ma
from webapp.soglasovanie.models import BusinessProcess, FileAttachment, SoglasovanieTask
from webapp.soglasovanie.views import blueprint as soglasovanie_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint

import logging

logging.basicConfig(filename='error.log',level=logging.DEBUG)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)
    migrate = Migrate(app, db)  # NOQA F841

    ma.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    login_manager.login_message = "Для доступа к сайту необходимо авторизоваться"

    app.register_blueprint(api_blueprint)
    app.register_blueprint(soglasovanie_blueprint)
    app.register_blueprint(user_blueprint)

    admin = Admin(app, "Настройки приложения", index_view=MyAdminIndexView())
    admin.add_view(MyUserView(User, db.session, name="Пользователи", endpoint="user_"))
    admin.add_view(MyBusinessProcessView(BusinessProcess, db.session, name="Бизнес-процессы", category="Задачи"))
    admin.add_view(MyModelView(SoglasovanieTask, db.session, name="Задачи", category="Задачи"))
    admin.add_view(MyModelView(FileAttachment, db.session, name="Файлы", category="Задачи"))

    register_my_jinja_filters(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.errorhandler(403)
    def error_handler_403(e):
        return render_template("errors/403.html", page_title="Ошибка"), 403

    @app.errorhandler(404)
    def error_handler_404(e):
        return render_template("errors/404.html", page_title="Ошибка"), 404

    @app.errorhandler(500)
    def error_handler_500(e):
        return render_template("errors/500.html", page_title="Ошибка"), 500

    app.register_error_handler(403, error_handler_403)
    app.register_error_handler(404, error_handler_404)
    app.register_error_handler(500, error_handler_500)

    return app
