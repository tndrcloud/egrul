from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy import create_engine
from settings import settings


Base = declarative_base()


class Company(Base):
    """class for describing the SQLAlchemy ORM model"""

    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, nullable=False)
    inn = Column(BigInteger, nullable=False)
    kpp = Column(BigInteger, nullable=False)
    address = Column(String, nullable=False)


engine_db = create_engine(settings.DB_PATH)
Base.metadata.create_all(engine_db)