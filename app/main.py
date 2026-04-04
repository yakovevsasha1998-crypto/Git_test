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
Base.metadata.drop_all(bind=engine)  # удалит все таблицы
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
        {"user_id": user.id, "exp": datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {
        "access_token": f'bearer {token}',
        "token_type": "bearer",
        "user_id": user.id,
        "status":'200 - все четко ты зашел!'
    }

def validen_token(valid_token:str = Header(...)):
    try:
        token = valid_token.replace('bearer ','')
        
        validation = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return validation.get('user_id')
    except:
        raise HTTPException(status_code=401,detail='Токен не валиден!')
   
@app.get('/get_all_user_task',tags=['Посмотреть список задач'])
def get_user_task(user_id:int = Depends(validen_token),db:Session = Depends(get_db)):
    
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    
    if not tasks:
        raise HTTPException(status_code=404,detail= 'нет задач у данного пользователя')
    return {
        'Всего задач':len(tasks),
        'tasks':tasks
    }
    
@app.post('/create_task',tags=['Добавить задачу'])
def create_task(
    task:CreateTask,db:Session = Depends(get_db),
    user_id:int = Depends(validen_token)
):
    new_task = Task(
        name_task = task.name_task,
        description = task.description,
        user_id = user_id
    )
    
    db.add(new_task)
    db.commit()
    return 'все четко задача добавлена'

@app.put('/put_task/{task_id}', tags=['Обновить задачу'])
def put_task(
    task_id: int,
    task_update: CreateTask,
    user_id: int = Depends(validen_token),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(404, 'Задача не найдена')
    
    if task.user_id != user_id:
        raise HTTPException(403, 'Это не твоя задача')
    
    # Обновляем и название, и описание
    task.name_task = task_update.name_task  
    task.description = task_update.description  
    task.is_completed = task_update.is_completed
    
    db.commit()
    db.refresh(task)
    
    return {
        "message": "Задача обновлена",
        "task": task
    }
    
@app.delete('/delete_task/{task_id}')
def delete_task(task_id:int,user_id:int = Depends(validen_token),db:Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=403,detail='Задача не найдена')
    
    db.delete(task)
    db.commit()
    db.refresh(task)
    
    return {
        'name':task.name_task,
        'description':task.description,
        'status':'успешно удалена'
    }
    
@app.get('/my_progile',tags=['мой профиль'])
def get_my_profil(user_id:int = Depends(validen_token),db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail='Пользователь не найден')
    task = db.query(Task).filter(Task.id == user_id).all()
    return {
        'username':user.username,
        'age':user.age,
        'bio':user.bio,
        'tasks': task,
        'tasks_count': len(task)
    }

