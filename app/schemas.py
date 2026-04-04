from pydantic import BaseModel,Field,EmailStr,SecretStr

#создаем пользователя
class UserCreate(BaseModel):
    username:str = Field(min_length=2,max_length=100)
    age:int = Field(ge=0,le=100)
    password:str
    bio:str|None = None


#вход в аккаунт  
class UserLogin(BaseModel):
    username:str = Field(min_length=2,max_length=100)
    password:str
    
#сздание задачи

class CreateTask(BaseModel):
    name_task:str 
    description:str | None = None
    

    

    
    