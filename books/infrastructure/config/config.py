from dataclasses import dataclass
import yaml


@dataclass
class DBConfig:
    file_name: str
    host: str
    port: int
    user: str
    password: str
    database: str
    mongo_uri: str
    mongo_db_name: str


@dataclass
class CacheConfig:
    host: str
    port: int
    password: str
    db: int


@dataclass
class ApplicationConfig:
    port: int
    page_size: int
    token_secret: str
    token_hours: int


@dataclass
class Config:
    app: ApplicationConfig
    cache: CacheConfig
    db: DBConfig


def parseConfig(filename: str) -> Config:
    with open(filename, 'r') as f:
        data = yaml.safe_load(f)
        return Config(
            ApplicationConfig(**data['app']),
            CacheConfig(**data['cache']),
            DBConfig(**data['db'])
        )
