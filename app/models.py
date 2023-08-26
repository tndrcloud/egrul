from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, JSON
from sqlalchemy import create_engine
from envparse import Env


env = Env()
env.read_envfile('.env')
db_path = env.str("DB_PATH")


Base = declarative_base()


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, nullable=False)
    inn = Column(BigInteger, nullable=False)
    kpp = Column(BigInteger, nullable=False)
    address = Column(String, nullable=False)


engine_db = create_engine(db_path)
Base.metadata.create_all(engine_db)