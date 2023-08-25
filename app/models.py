from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy import create_engine
from envparse import Env


env = Env()
env.read_envfile('.env')


Base = declarative_base()


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    code = Column(String)
    inn = Column(Integer(10))
    kpp = Column(Integer(9))
    address = Column(JSON)


engine_db = create_engine(env.str("DB_PATH"))
Base.metadata.create_all(engine_db)