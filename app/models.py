from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, JSON
from sqlalchemy import create_engine
from envparse import Env


env = Env()
env.read_envfile('.env')


Base = declarative_base()


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, autoincrement=True)
    name = Column(String(100), primary_key=True)
    code = Column(String, nullable=True)
    inn = Column(BigInteger, nullable=True)
    kpp = Column(BigInteger, nullable=True)
    address = Column(JSON, nullable=True)


engine_db = create_engine(env.str("DB_PATH"))
Base.metadata.create_all(engine_db)