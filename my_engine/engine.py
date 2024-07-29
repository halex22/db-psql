from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_USER = getenv('DB_USER')
DB_PASS = getenv('DB_PASS')
DB_NAME = getenv('DB_NAME')


engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@localhost:5433/{DB_NAME}")


Session = sessionmaker(bind=engine)
session = Session()

__all__ = ['session']