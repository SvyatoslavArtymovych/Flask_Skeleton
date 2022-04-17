import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(environment="development"):

    from config import config
    from app.models import User, AnonymousUser

    # Instantiate app.
    app = Flask(__name__)

    # Set app config.
    env = os.environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])
    config[env].configure(app)
    app.config["VALIDATE_RESPONSE"] = True

    # Set up extensions.
    db.init_app(app)
    login_manager.init_app(app)

    # Register bluerint
    from app.views import (
        auth_blueprint,
    )

    app.register_blueprint(auth_blueprint)

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id):
        return User.query.get(int(id))

    login_manager.login_view = "/login"
    login_manager.login_message_category = "info"
    login_manager.anonymous_user = AnonymousUser

    Migrate(app, db)
    return app
