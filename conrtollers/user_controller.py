from sqlalchemy import exc
from werkzeug import exceptions
from flask import request
from helpers.json import json_response
from models.user import User
from database.connect import db_session


def create(req: request):
    user_el = User(
        email=req.form['email'],
        password=req.form['password']
    )
    try:
        db_session.add(user_el)
        db_session.commit()
    except exc.SQLAlchemyError as e:
        return json_response(str(e), 'error', 500)

    response = json_response()
    return response


def read(req: request):
    args = req.args.to_dict()

    try:
        users = User.query.filter_by(**args).all()
    except exc.InvalidRequestError as e:
        return json_response(str(e), 'error', 500)

    return json_response(users)


def update(req: request):
    req_id = req.args.get('id')
    fields = req.form.to_dict()

    if not req_id:
        return json_response("`id` is require param in query", 'error', 404)
    try:
        int_id = int(req_id)
    except ValueError:
        return json_response(f'Impossible to convert `{req_id}` to Integer', 'error', 500)

    count = User.query.filter(User.id == int_id).update(fields)
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

    count = User.query.filter(User.id == int_id).delete()
    if not count:
        return json_response(f'Not found records with `id` = `{int_id}`', 'error', 404)
    db_session.commit()

    return json_response()
