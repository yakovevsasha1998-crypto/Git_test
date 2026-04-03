from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autoflush = False,autocommit = False,bind=engine)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    except Exception as e:
        print(f'Ошибка подлкючения к бд{e}')
        db.rollback()
        raise
    finally:
        db.close()