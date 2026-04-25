from sqlalchemy import Column, Integer, String ,Float,TIMESTAMP, text
from .database import Base

class Student(Base):
    __tablename__ = "local_student"

   
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False)
    dept = Column(String, nullable=False)
    sem = Column(Integer, nullable=False)
    email = Column(String, nullable=False)


class Stoners(Base):
    __tablename__ = "stoners"

   
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False)
    sem = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
