from dataclasses import dataclass


@dataclass
class UserCredential:
    email: str
    password: str


@dataclass
class User:
    id: int
    email: str
