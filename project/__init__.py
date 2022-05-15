import os.path
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4
from flask_migrate import Migrate
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
migrate = Migrate()


def create_app():

    STATIC_DIR = os.path.abspath('static')

    app = Flask(__name__, static_folder=STATIC_DIR)

    app.config['SECRET_KEY'] = os.urandom(12).hex()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Bootstrap4(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for  parts of app witch need auth
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
