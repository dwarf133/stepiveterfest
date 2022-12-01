import os

from flask import Flask
from database.connect import init_db
from helpers.model_encoder import ModelEncoder
from models.user import User
from routes.web import app_route
from routes.web import app_route
from dotenv import load_dotenv
from celery import Celery
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="",
    template_folder='templates'
)

app.register_blueprint(app_route)
app.json_encoder = ModelEncoder


def init():
    app = Flask(
        __name__,
        static_folder="templates",
        static_url_path="",
        template_folder='templates'
    )
    app.register_blueprint(app_route)
    app.json_encoder = ModelEncoder
    CORS(app)
    load_dotenv('.env')
    init_db()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app


if __name__ == '__main__':
    init().run(debug=True)
