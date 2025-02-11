from typing import Annotated, Generic, List, TypeVar
from pydantic import BaseModel
from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session
from fastapi import Depends


class PaginationParameters(BaseModel):
    page: int
    per_page: int


M = TypeVar("M")


class PaginationResponseSchema(BaseModel, Generic[M]):
    total: int
    items: List[M]


PaginationDependency = Annotated[PaginationParameters, Depends()]


def paginate(session: Session, query: Select, pagination: PaginationParameters):

    items = session.scalars(
        query.offset((pagination.page - 1) * pagination.per_page).limit(
            pagination.page * pagination.per_page
        )
    ).all()

    total = session.scalar(select(func.count()).select_from(query.subquery()))

    return {
        "items": items,
        "total": total,
    }
