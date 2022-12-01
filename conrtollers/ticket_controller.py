from sqlalchemy import exc
from werkzeug import exceptions
from flask import request, render_template
from helpers.json import json_response
from models.ticket import Ticket
from database.connect import db_session
from datetime import datetime
from flask_login import current_user


def create(req: request):
    ticket_el = Ticket(
        seed=req.form['seed'],
        order_id=req.form['order_id'],
        email=req.form['email'],
        phone=req.form['phone'],
    )
    try:
        db_session.add(ticket_el)
        db_session.commit()
    except exc.SQLAlchemyError as e:
        return json_response(str(e), 'error', 500)

    response = json_response()
    return response


def read(req: request):
    args = req.args.to_dict()

    try:
        tickets = Ticket.query.filter_by(**args).all()
    except exc.InvalidRequestError as e:
        return json_response(str(e), 'error', 500)

    return json_response(tickets)


def update(req: request):
    req_id = req.args.get('id')
    fields = req.form.to_dict()

    if not req_id:
        return json_response("`id` is require param in query", 'error', 404)
    try:
        int_id = int(req_id)
    except ValueError:
        return json_response(f'Impossible to convert `{req_id}` to Integer', 'error', 500)

    count = Ticket.query.filter(Ticket.id == int_id).update(fields)
    if not count:
        return json_response(f'Not found records with `id` = `{int_id}`', 'error', 404)
    db_session.commit()

    return json_response()


def delete(req: request):
    try:
        req_id = req.form['id']
    except exceptions.BadRequestKeyError:
        return json_response("`id` is require field", 'error', 404)
    if not req_id:
        return json_response("`id` is require field", 'error', 404)

    try:
        int_id = int(req_id)
    except ValueError:
        return json_response(f'Impossible to convert `{req_id}` to Integer', 'error', 500)

    count = Ticket.query.filter(Ticket.id == int_id).delete()
    if not count:
        return json_response(f'Not found records with `id` = `{int_id}`', 'error', 404)
    db_session.commit()

    return json_response()


def check(req: request):
    args = req.args.to_dict()
    try:
        ticket = Ticket.query.filter_by(**args).first()
    except exc.InvalidRequestError as e:
        return render_template('auth/check_error.html')

    if current_user.is_authenticated:
        last_usage = ticket.last_usage
        Ticket.query.filter_by(**args).update({Ticket.last_usage: datetime.now()})
        db_session.commit()

        ticket.last_usage = last_usage

        return render_template('auth/check.html',
                               ticket_type=ticket.ticket_type,
                               email=ticket.email,
                               phone=ticket.phone,
                               last_usage=ticket.last_usage,
                               )
    else:
        return render_template('auth/check.html', ticket_type=ticket.ticket_type)
