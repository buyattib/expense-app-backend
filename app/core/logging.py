from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import sys

logger = logging.getLogger()

formatter = logging.Formatter(fmt="%(levelname)s %(asctime)s - %(message)s")

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# file_handler = logging.FileHandler("app.log")
# file_handler.setFormatter(formatter)

logger.handlers = [
    stream_handler,
    # file_handler
]

logger.setLevel(logging.INFO)


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method

        if method != "GET":
            pass
        else:
            pass

        headers = request.headers
        client = request.client

        log = {
            "path": request.url.path,
            "method": method,
            "ip": client.host if client else None,
            "port": client.port if client else None,
            "origin": headers["origin"],
            "user-agent": headers["user-agent"],
            "platform": headers.get("sec-ch-ua-platform"),
        }

        logger.info(log, extra=log)

        response = await call_next(request)

        return response
