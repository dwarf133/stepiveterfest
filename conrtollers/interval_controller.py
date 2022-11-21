from helpers.json import json_response
from sqlalchemy import exc
from models.time_intervals import TimeIntervals, Guests


POSSIBLE_TYPES = ["tattoes", "walk", "peppers", "lambik"]

def get_possible_time(type: str):
    if type in POSSIBLE_TYPES:
        intervals = TimeIntervals.select_vacant_by_type(type=type)
        return json_response(intervals)
    else:
        return json_response(f'Unknown `{type}`', 'error', 500)
    
def order_interval(req: dict):
    interval = TimeIntervals.select_interval_by_time(time=req['time'], type=req['type'])
    if not(isinstance(interval, exc.InvalidRequestError)):
        guest = Guests(name=req['name'], surname=req['surname'], phone=req['phone'], email=req['email'], interval_id=interval.id)
        err = guest.create(interval=interval)
        if isinstance(err, exc.SQLAlchemyError):
            return json_response('Time interval already ordered')
        else: 
            return json_response('Succefuly ordered')
    else:
        return json_response('Time interval already ordered')