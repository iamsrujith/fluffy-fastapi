from typing import Any, Optional
from sqlalchemy import create_engine, types
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY = "postgresql://postgres:aadhi@localhost/fluffy"

engine = create_engine(
    SQLALCHEMY
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
