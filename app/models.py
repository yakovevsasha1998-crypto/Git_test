from sqlalchemy import Column,Integer,String,DateTime,Boolean
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
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
    user_id = Column(Integer,nullable=False)
    is_completed = Column(Boolean,default=False)
    
    
    

