from sqlalchemy.ext.declarative import declarative_base
from db import engine

Base = declarative_base(engine)