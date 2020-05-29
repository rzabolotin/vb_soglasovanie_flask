from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from webapp.model import db
from webapp.soglasovanie.views import blueprint as soglasovanie_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Для доступа к сайту необходимо авторизоваться'

    app.register_blueprint(soglasovanie_blueprint)
    app.register_blueprint(user_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
        
    return app
