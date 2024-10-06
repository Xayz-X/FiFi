
from typing import TypedDict


class Bot(TypedDict):
    token: str
    debug: bool


class Config(TypedDict):
    BOT: Bot
