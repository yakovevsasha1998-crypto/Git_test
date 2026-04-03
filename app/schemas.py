from pydantic import BaseModel,Field,EmailStr,SecretStr

class UserCreate(BaseModel):
    
    