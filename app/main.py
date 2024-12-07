from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.lib.utils import parse_cors
from app.core.database import Base, engine
from app.core.logging import logger, LoggerMiddleware
from app.core.rate_limiting import RateLimiterMiddleware

# routers
from app.auth.endpoints import router as auth_router
from app.user.endpoints import router as user_router

from app.transaction.endpoints import (
    transaction_category_router,
    transaction_router,
)
from app.account.endpoints import currency_router, account_router, account_type_router


logger.info("Initializing app...")

# init fast api app
app = FastAPI(
    root_path=f"/api/{settings.api_version}",
)


# create database: delete this when using migrations with alembic
Base.metadata.create_all(bind=engine)

# middleware -----------

app.add_middleware(LoggerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=parse_cors(settings.backend_cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimiterMiddleware)


# routers -----------

app.include_router(auth_router)
app.include_router(user_router)

app.include_router(currency_router)
app.include_router(account_router)
app.include_router(account_type_router)

app.include_router(transaction_category_router)
app.include_router(transaction_router)


@app.get("/")
def hello_world():
    return {"message": "OK"}


# TODO: if i want to use cookies to send the access token in the requests, i can make a middleware to get the cookie and set the access token in the headers, in that way the routes that use the auth dependency will work
