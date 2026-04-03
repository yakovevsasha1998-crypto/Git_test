import bcrypt
import jwt
from database import get_db
from fastapi import Depends,HTTPException

def heshed_password(password:str)-> str:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    