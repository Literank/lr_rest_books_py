from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    email: str
    password: str
    salt: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime
