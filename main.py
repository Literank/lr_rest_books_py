from flask import Flask

from books.adapter.router import make_router
from books.application import WireHelper
from books.infrastructure.config import Config, ApplicationConfig, DBConfig

c = Config(
    ApplicationConfig(
        8080
    ),
    DBConfig(
        "test.db"
    )
)
wire_helper = WireHelper.new(c)
app = Flask(__name__)
make_router(app, wire_helper)
