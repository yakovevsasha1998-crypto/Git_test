from fastapi import FastAPI, HTTPException, Depends,Header
from sqlalchemy.orm import Session
from datetime import datetime,timedelta
import bcrypt
import jwt
from database import get_db, Base, engine
from schemas import UserCreate, UserLogin, CreateTask
from models import User, Task
import dotenv
import uvicorn

from config import DB, ALGORITHM, TOKEN_TIME, SECRET_KEY

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post('/Зарегистрироваться', tags=['Регистрация пользователя'])
def register_users(user: UserCreate, db: Session = Depends(get_db)):
    
    # Проверка имени
    user_valid = db.query(User).filter(User.username == user.username).first()
    if user_valid:
        raise HTTPException(status_code=409, detail='Данное имя уже занято, введите другое имя!')
    
    # Проверка возраста
    if user.age < 18:
        raise HTTPException(status_code=422, detail='Вам должно быть больше 18')
    
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'),
        bcrypt.gensalt()
    )
    
    new_user = User(
        username=user.username,
        password=hashed_password.decode('utf-8'),
        age=user.age,
        bio=user.bio
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "Пользователь зарегистрирован",
        "user_id": new_user.id
    }
    
@app.post('/Авторизация', tags=['Авторизация пользователя'])
def login_user(login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.username == login.username
    ).first()
    
    if not user:
        raise HTTPException(status_code=401, detail='Пользователь не найден')
    
    if not bcrypt.checkpw(login.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail='Неверный пароль')
    
    token = jwt.encode(
        {"sub": user.id, "exp": datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "status":'200 - все четко ты зашел!'
    }

def validen_token()