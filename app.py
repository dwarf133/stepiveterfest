import os

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
from flask import jsonify
from flask import request

app = Flask(__name__, static_url_path="/", static_folder='templates')

db_connection = os.environ.get('DB_CONNECTION')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')

try:
    database_uri = 'postgresql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name
except():
    print('wrong connect data')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name

db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seed = db.Column(db.String, unique=True)
    order_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    __tablename__ = "tickets"

    def __repr__(self):
        return '<Ticket %r : %r>' % self.email, self.seed

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template('/index.html')


@app.route("/order", methods=["POST"])
def order():
    pass


@app.route("/tickets")
def tickets():
    ticket_list = db.select(Ticket)
    res = []
    with db.engine.connect() as conn:
        for row in conn.execute(ticket_list):
            res.append(row)
    return jsonify({'result': [dict(row) for row in res]})


@app.route("/ticket", methods=['POST'])
def ticket():
    ticket_el = Ticket(
        seed=request.form['seed'],
        order_id=request.form['order_id'],
        email=request.form['email'],
        phone=request.form['phone'],
    )

    res = db.session.add(ticket_el)
    print(res)
    res = db.session.commit()
    print(res)

    return 'success'


# @app.route("/ticket", methods=['POST'])
# def create_ticket():
#     if request.method == 'POST':
#         ticket_el = Tickets('123', '123', '123')
#         db.session.add(ticket_el)
#         db.session.commit()
#     else:
#         return 'else'
#
#     return 'asd'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
