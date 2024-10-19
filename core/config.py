from __future__ import annotations
import toml
from typing import Any

__all__: tuple[str, ...] = ("CONFIG",)


class BotConfig:
    def __init__(self, token: str, debug: bool):
        self.token = token
        self.debug = debug


class DatabaseConfig:
    def __init__(self, dsn: str):
        self.dsn = dsn


class ConfigNode:
    def __init__(self, bot: BotConfig, database: DatabaseConfig):
        self.BOT = bot
        self.DATABASE = database

    @staticmethod
    def from_dict(data: dict[str, Any]) -> ConfigNode:
        bot_data = data.get("BOT", {})
        database_data = data.get("DATABASE", {})

        bot_config = BotConfig(
            token=bot_data.get("token", ""),
            debug=bot_data.get("debug", False),
        )
        database_config = DatabaseConfig(
            dsn=database_data.get("dsn", ""),
        )

        return ConfigNode(bot=bot_config, database=database_config)


def load_config(file_path: str) -> ConfigNode:
    try:
        with open(file_path, "r") as fp:
            data = toml.load(fp)
            return ConfigNode.from_dict(data)
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file {file_path} not found.")
    except toml.TomlDecodeError:
        raise RuntimeError(f"Error decoding TOML file {file_path}.")


CONFIG: ConfigNode = load_config("config.toml")
