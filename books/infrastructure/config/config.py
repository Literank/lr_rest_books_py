from dataclasses import dataclass


@dataclass
class DBConfig:
    file_name: str
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass
class ApplicationConfig:
    port: int


@dataclass
class Config:
    app: ApplicationConfig
    db: DBConfig
