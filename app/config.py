from dotenv import load_dotenv
import os

load_dotenv()

DB = os.getenv('DATABASE_URL')
ALGORITHM = os.getenv('Algorithm')
TOKEN_TIME = os.getenv('TOKEN_TIME')
SECRET_KEY = os.getenv('SECRET_KEY')