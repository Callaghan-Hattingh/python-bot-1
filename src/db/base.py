from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from src.core import config

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = f"sqlite:///data/{config.currency_pair}.db?journal_mode=WAL"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
session = Session(bind=engine)


def create_tables():
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
