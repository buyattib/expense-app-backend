from typing import Union
import uuid


def parse_cors(v: Union[str, None]) -> list[str]:
    if not v:
        return []
    return [i.strip() for i in v.split(",")]


def generate_uuid():
    """Generate a new UUID as a string for SQLite compatibility"""
    return str(uuid.uuid4())
