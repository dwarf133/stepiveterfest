from flask import Blueprint, make_response
from flask import request
from flask import render_template
from conrtollers import qr_controller
from conrtollers import ticket_controller
from helpers.json import json_response
import tasks

from conrtollers import ticket_controller, user_controller

app_route = Blueprint('route', __name__)


# --- Web Routes --- #

@app_route.route("/")
def index():
    return render_template('main/index.html')


@app_route.route("/login")
def login():
    return render_template('auth/index.html')


# --- Api Routes --- #

@app_route.route("/order", methods=["POST"])
def order():
    tasks.qr_tasks.delay(int(request.form['id']))
    # qr_controller.proceed_order(int(request.form['id']))
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


@app_route.post("/user")
def user_create():
    return user_controller.create(request)


@app_route.get("/users")
def users_read():
    return user_controller.read(request)


@app_route.patch("/user")
def user_update():
    return user_controller.update(request)


@app_route.delete("/user")
def user_delete():
    return user_controller.delete(request)