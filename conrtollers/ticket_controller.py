import sqlalchemy
from sqlalchemy import exc
from flask import request
from helpers.json import json_response
from models.ticket import Ticket
from database.connect import db_session
from database.connect import Base


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
    pass


def delete(req: request):
    pass
