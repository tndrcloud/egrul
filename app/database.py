from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert
from models import engine_db
from models import Company
from log import logger


class Operations:
    """class with database operations"""

    def add_company(data):
        with engine_db.connect() as session:
            try:
                statement = insert(Company).values(**data)
                session.execute(statement)
                session.commit()
                logger.info("add data succesfully")
                
            except IntegrityError:
                logger.info('pass duplicate')
