from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.connect import Base
from database.connect import db_session
from sqlalchemy import exc

class TimeIntervals(Base):
    __tablename__ = 'intervals'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


    def __init__(self, id, name, surname, phone, email) -> None:
        self.id = id
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email
    

    def create(self):
        try:
            db_session.add(self)
            db_session.commit()
        except exc.SQLAlchemyError as e:
            return e
        return self 

    
    
        