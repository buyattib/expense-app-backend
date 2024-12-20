from datetime import datetime

from fastapi import Depends
from typing import Annotated
from sqlalchemy import MetaData, create_engine, DateTime, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.sql import func

from app.config import settings


# Connection to db
engine = create_engine(
    url=settings.sqlalchemy_database_uri,
    echo=True,
    connect_args={"check_same_thread": False},  # only for sqlite
)


# only for sqlite
@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


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
    # created: Mapped[datetime] = mapped_column(
    #     TIMESTAMP(timezone=True),
    #     server_default=func.now(),
    #     server_default=text("now()"),
    # )
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
