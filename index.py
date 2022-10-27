from flask import Flask
from flask import render_template
from db.app import Tickets
from db.app import db
from flask import request

app = Flask(__name__, static_url_path="/", static_folder='templates')


@app.route("/")
def index():
    return render_template('/index.html')


@app.route("/ticket/<seed>", )
def ticket(seed):
    ticket_el = Tickets.query.filter_by(seed=seed).first_or_404()
    return str(ticket_el)
    # print(tickets)


@app.route("/ticket", methods=['POST'])
def create_ticket():
    if request.method == 'POST':
        ticket_el = Tickets('123', '123', '123')
        db.session.add(ticket_el)
        db.session.commit()
    else:
        return 'else'

    return 'asd'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
