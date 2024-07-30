from models import Base
from my_engine import engine, session

Base.metadata.create_all(engine)
