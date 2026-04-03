from sqlalchemy import Column,Integer,String,DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    email = Column(String(100),unique=True,nullable=False,index=True)
    username = Column(String(50),unique=True,index=True,nullable=False)
    password = Column(String,nullable=False)
    age = Column(Integer)
    created_account = Column(DateTime,default=datetime.utcnow())
    bio = Column(String)
class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer,primary_key=True)
    name_task = Column(String(50),index=True)
    description = Column(String)
    
    

