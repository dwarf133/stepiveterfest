from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.connect import Base
from flask_login import UserMixin


class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __init__(self, id=None, email=None, password=None, created_at=None, updated_at=None):
        self.id = id
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f'<Ticket ' \
               f'id: {self.id!r}, ' \
               f'email: {self.email!r} , ' \
               f'password: {self.password!r} , ' \
               f'created_at: {self.created_at!r} , ' \
               f'updated_at: {self.updated_at!r}'

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def is_active(self):
        return True
