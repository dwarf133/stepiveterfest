import os

from flask import Flask
from database.connect import init_db
from helpers.model_encoder import ModelEncoder
from routes.web import app_route
from dotenv import load_dotenv



def init():
    app = Flask(__name__, static_url_path="/", static_folder='templates')
    app.register_blueprint(app_route)
    app.json_encoder = ModelEncoder
    load_dotenv('.env')
    init_db()
    return app


if __name__ == '__main__':
    init().run(debug=True, host='0.0.0.0')
