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


@app_route.post("/ticket")
def ticket_create():
    return ticket_controller.create(request)


@app_route.get("/tickets")
def tickets_read():
    return ticket_controller.read(request)


@app_route.patch("/ticket")
def ticket_update():
    return ticket_controller.update(request)


@app_route.delete("/ticket")
def ticket_delete():
    return ticket_controller.delete(request)
