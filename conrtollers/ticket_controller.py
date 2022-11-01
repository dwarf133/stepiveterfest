from sqlalchemy import exc
from flask import request, make_response, jsonify
from helpers.json import json_response
from models.ticket import Ticket
from database.connect import db_session


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
    tickets = Ticket.query.all()
    response = make_response(
        jsonify(
            {
                "status": "success",
                "data": tickets
            }
        ),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


def update(req: request):
    pass


def delete(req: request):
    pass
