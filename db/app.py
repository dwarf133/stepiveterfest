import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func

app = Flask(__name__)

db_connection = os.environ.get('DB_CONNECTION')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')

try:
    database_uri = f'postgresql://{db_user}:{db_pass}@{db_host}/{db_name}'
except:
    print('wrong connect data')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}/{db_name}'

db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)


class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seed = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    def __repr__(self):
        return '<Ticket %r : %r>' % self.email, self.seed
