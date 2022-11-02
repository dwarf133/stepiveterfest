import json
from flask import Blueprint, make_response
from flask import request
from flask import render_template
from conrtollers import qr_controller
from conrtollers import ticket_controller
from helpers.json import json_response

app_route = Blueprint('route', __name__)


# --- Web Routes --- #

@app_route.route("/")
def index():
    return render_template('/index.html')


# --- Api Routes --- #

@app_route.route("/order", methods=["POST"])
def order():
    qr_controller.proceed_order(int(request.form['id']))
    return json_response()


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
