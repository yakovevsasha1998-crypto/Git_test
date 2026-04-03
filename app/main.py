from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db,Base,engine
from schemas import UserCreate,UserLogin,CreateTask
from models import User,Task
from auth import heshed_password

app = FastAPI()

@app.post('/Зарегестрироваться',tags=['Регистрация пользователя'])
def register_users(user:UserCreate,db:Session=Depends(get_db)):
    user_valid = db.query(User).filter(User.username == user.username)
    if user_valid:
        raise HTTPException(status_code=409,detail='Данное имя уже занято,введите другое имя!')
    
