from datetime import datetime

from fastapi import Depends
from typing import Annotated
from sqlalchemy import MetaData, create_engine, DateTime, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.sql import func

from app.config import settings

"""
+driver and /database are optional (database is the name of the db). Common drivers: psycopg2, pg8000

pg connection string: postgresql+driver://user:password@host:port/database

example: postgresql://bautista:pg123abc@localhost:5433/postgres # from host
example: postgresql://bautista:pg123abc@localhost:5432/postgres # from compose
example: postgresql://bautista:pg123abc@container-name/postgres # from compose
"""

# Connection to db
engine = create_engine(
    url=str(settings.sqlalchemy_database_uri),
    # echo=True,
    # connect_args={"check_same_thread": False},  # only for sqlite
)


# Session passed to each endpoint
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


# Base model inherited by all the rest
class Base(DeclarativeBase):
    metadata = metadata
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]
