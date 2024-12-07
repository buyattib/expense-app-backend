import time
from typing import Optional, Union
from fastapi import BackgroundTasks, Request, Response
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_429_TOO_MANY_REQUESTS

from app.core.logging import logger


class RateLimitErrorSchema(BaseModel):
    code: int
    message: str


class RateLimitError(Exception):
    NO_IP = RateLimitErrorSchema(
        code=HTTP_400_BAD_REQUEST, message="No ip in the request"
    )
    EXCEEDED = RateLimitErrorSchema(
        code=HTTP_429_TOO_MANY_REQUESTS, message="Rate limit exceeded"
    )

    def __init__(self, err: RateLimitErrorSchema, ip: Optional[str] = None):
        super().__init__(err.message)
        logger.error(f"RateLimitError{' - ' + ip if ip else ''}: {err.message}")

        self.code = err.code
        self.message = err.message
        self.ip = ip


# could improve this using a database or cache like redis


class RateLimiter:
    def __init__(self, requests_per_second: Union[int, float]):
        # rate_limit_records: { "ip": { "last_request": timestamp, "requests_number": float } }
        self.rate_limit_records: dict[str, dict[str, float]] = {}
        self.unlimited_requests_ip = []
        self.requests_per_second = requests_per_second
        # self.unlimited_requests_ip = ["127.0.0.1"]

    def cleanup(self):
        current_time = time.time()
        seconds_in_week = 24 * 60 * 60
        updated_records = {}
        for ip, values in self.rate_limit_records.items():
            if abs(current_time - values["last_request"]) < seconds_in_week:
                updated_records[ip] = values
            else:
                logger.info(f"Cleaning up ip: {ip}")

        self.rate_limit_records = updated_records

    def check_requests_limits(self, request: Request):
        current_time = time.time()

        client_ip = request.client.host if request.client else None
        if not client_ip:
            raise RateLimitError(RateLimitError.NO_IP)

        if client_ip in self.unlimited_requests_ip:
            return

        if client_ip not in self.rate_limit_records:
            self.rate_limit_records[client_ip] = {
                "last_request": current_time,
                "requests_number": 1,
            }
            return

        seconds = 1 / self.requests_per_second
        not_enough_time_passed = (
            current_time - self.rate_limit_records[client_ip]["last_request"] < seconds
        )
        request_number_exceeded = (
            self.rate_limit_records[client_ip]["requests_number"]
            > self.requests_per_second
        )

        if not_enough_time_passed and request_number_exceeded:
            raise RateLimitError(RateLimitError.EXCEEDED, ip=client_ip)

        if not not_enough_time_passed and request_number_exceeded:
            self.rate_limit_records[client_ip]["last_request"] = current_time
            self.rate_limit_records[client_ip]["requests_number"] = 1
            return

        self.rate_limit_records[client_ip]["last_request"] = current_time
        self.rate_limit_records[client_ip]["requests_number"] += 1

        return

    def __call__(self, request: Request):
        """
        Example:
        limiter = RateLimiter(requests_per_second=5)

        As dependency:
        is_allowed: Annotated[bool, Depends(limiter)]
        """

        try:
            self.check_requests_limits(request)
            return True
        except RateLimitError:
            return False


class RateLimiterMiddleware(BaseHTTPMiddleware):
    GLOBAL_LIMIT_REQUESTS_PER_SECOND = 50

    def __init__(self, app):
        super().__init__(app)
        self.limiter = RateLimiter(self.GLOBAL_LIMIT_REQUESTS_PER_SECOND)

    async def dispatch(self, request: Request, call_next):
        try:
            self.limiter.check_requests_limits(request)

            background_tasks = BackgroundTasks()
            background_tasks.add_task(self.limiter.cleanup)

            response = await call_next(request)
            response.background = background_tasks

            return response
        except RateLimitError as e:
            return Response(status_code=e.code, content=e.message)
