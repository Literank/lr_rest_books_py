from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum


@dataclass
class User:
    id: int
    email: str
    password: str
    salt: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class UserPermission(IntEnum):
    PermNone = 0
    PermUser = 1
    PermAuthor = 2
    PermAdmin = 3
