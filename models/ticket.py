from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.connect import Base
from database.connect import db_session
from sqlalchemy import exc


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    seed = Column(String, unique=True)
    order_id = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __init__(self, id=None, seed=None, order_id=None, email=None, phone=None, created_at=None, updated_at=None):
        self.id = id
        self.phone = phone
        self.email = email
        self.order_id = order_id
        self.seed = seed
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f'<Ticket ' \
               f'id: {self.id!r}, ' \
               f'order_id: {self.order_id!r}, ' \
               f'phone: {self.phone!r} , ' \
               f'email: {self.email!r} , ' \
               f'seed: {self.seed!r}> '

    def to_json(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "phone": self.phone,
            "email": self.email,
            "seed": self.seed,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def create(self):
        try:
            db_session.add(self)
            db_session.commit()
        except exc.SQLAlchemyError as e:
            return e
        return self 

    def read(order_id: int):
        try:
            tickets = Ticket.query.filter_by(order_id=order_id).all()
        except exc.InvalidRequestError as e:
            return e
        return tickets