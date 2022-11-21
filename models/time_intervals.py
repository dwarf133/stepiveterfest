from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.connect import Base
from database.connect import db_session
from sqlalchemy import exc
import time

class TimeIntervals(Base):
    __tablename__ = 'intervals'
    
    id = Column(Integer, primary_key=True)
    time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    vacant = Column(bool, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


    def __init__(self, id, time, type, vacant, created_at, updated_at) -> None:
        self.id = id
        self.time = time
        self.type = type
        self.vacant = vacant
        self.created_at = created_at
        self.updated_at = updated_at

    

    def create(self):
        try:
            db_session.add(self)
            db_session.commit()
        except exc.SQLAlchemyError as e:
            return e
        return self 

    def select_interval_by_id(id: Integer):
        try:
            interval = TimeIntervals.query.filter_by(id=id).one()
        except exc.InvalidRequestError as e:
            return e
        return interval

    def select_interval_by_time(time: String, type: String):
        try:
            interval = TimeIntervals.query.filter_by(time=time, type=type, vacant=True).one()
        except exc.InvalidRequestError as e:
            return e
        return interval

    def select_vacant_by_type(type: String):
        try:
            intervals = TimeIntervals.query.filter_by(type=type, vacant=True).all()
        except exc.InvalidRequestError as e:
            return e
        return intervals

    def make_not_vacant(self):
        try:
            self.vacant = False
            db_session.commit()
        except exc.SQLAlchemyError as e:
            return e
        return self 
    
    def first_execute():
        pass

    def to_json(self):
        return {
            "id": self.id,
            "time": self.time,
            "vacant": self.vacant,
            "type": self.type,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Guests(Base):
    
    __tablename__ = 'guests'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    inteval_id = Column(Integer, ForeignKey("intervals.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __init__(self, id, name, surname, phone, email, interval_id, created_at, updated_at) -> None:
        self.id = id
        self.name = name
        self.surname = surname, 
        self.phone = phone,
        self.email = email, 
        self.interval_id = interval_id
        self.created_at = created_at
        self.updated_at = updated_at

    def create(self, interval: TimeIntervals):
        try:
            if interval.vacant:
                interval.make_not_vacant()
                db_session.add(self)
                db_session.commit()
        except exc.SQLAlchemyError as e:
            return e
        return self

