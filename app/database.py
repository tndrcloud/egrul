from sqlalchemy import insert
from models import engine_db
from models import Company
from log import logger


class Operations:
    def add_company(data):
        with engine_db.connect() as session:
            statement = insert(Company).values(**data)
            session.execute(statement)
            session.commit()
            logger.info("add data succesfully")
