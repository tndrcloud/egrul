import json
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert
from models import engine_db
from models import Company
from log import logger


class Operations:
    """class with database operations"""
    
    def __init__(self) -> None:
        self.connector = engine_db

    def add_company(self, data: json) -> None:
        with self.connector.connect() as session:
            try:
                statement = insert(Company).values(**data)
                session.execute(statement)
                session.commit()
                logger.info(f"{data} add succesfully")
                
            except IntegrityError:
                logger.info(f"{data} pass duplicate")
