from flask import Flask
from flask_migrate import Migrate

from webapp.model import db
from webapp.soglasovanie.views import blueprint as soglasovanie_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(soglasovanie_blueprint)
    
    return app
