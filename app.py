import os

from flask import Flask
from database.connect import init_db
from helpers.model_encoder import ModelEncoder
from routes.web import app_route
from dotenv import load_dotenv

# Роут для отдачи статик файлов

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="",
    template_folder='templates'
)

app.register_blueprint(app_route)
app.json_encoder = ModelEncoder


if __name__ == '__main__':
    load_dotenv('.env')
    init_db()
    app.run(debug=True, host='0.0.0.0')
