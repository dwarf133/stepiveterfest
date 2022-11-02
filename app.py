from flask import Flask
from database.connect import init_db
from helpers.model_encoder import ModelEncoder
from routes.web import app_route

app = Flask(__name__, static_url_path="/", static_folder='templates')

app.register_blueprint(app_route)
app.json_encoder = ModelEncoder


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
