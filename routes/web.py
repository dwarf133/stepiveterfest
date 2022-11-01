from flask import Blueprint
from flask import request
from flask import render_template

from conrtollers import ticket_controller

app_route = Blueprint('route', __name__)


# --- Web Routes --- #

@app_route.route("/")
def index():
    return render_template('/index.html')


# --- Api Routes --- #

@app_route.route("/order", methods=["POST"])
def order():
    pass


@app_route.get("/tickets")
def tickets():
    return ticket_controller.read(request)


@app_route.post("/ticket")
def ticket():
    return ticket_controller.create(request)
