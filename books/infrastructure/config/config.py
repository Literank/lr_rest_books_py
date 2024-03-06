from dataclasses import dataclass


@dataclass
class DBConfig:
    file_name: str


@dataclass
class ApplicationConfig:
    port: int


@dataclass
class Config:
    app: ApplicationConfig
    db: DBConfig
