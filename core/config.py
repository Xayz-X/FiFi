from __future__ import annotations
import toml
from typing import Any
from pathlib import Path


__all__: tuple[str, ...] = ("CONFIG",)


class BotConfig:
    """
    A configuration for the bot.

    Attributes
    ----------
    token : `str`
        The bot token.
    debug : `bool`
        Whether the bot is in debug mode.
    version : `str`
        The bot version.
    exception_webhook : `str`
        The webhook to send errors to.
    owner_id : `int`
        The owner ID.
    """

    def __init__(
        self,
        token: str,
        debug: bool,
        version: str,
        exception_webhook: str,
        owner_id: int,
    ) -> None:
        self.token: str = token
        self.debug: bool = debug
        self.version: str = version
        self.exception_webhook: str = exception_webhook
        self.owner_id: int = (
            owner_id  # This is not required because we can get it from app info. It's just optional.
        )

    def __str__(self) -> str:
        return self.token

    def __repr__(self) -> str:
        return f"<BotConfig debug={self.debug} version={self.version}>"


class DatabaseConfig:
    """
    A configuration for the database.

    Attributes
    ----------
    dsn : `str`
        The database connection string.
    """

    def __init__(self, dsn: str) -> None:
        self.dsn: str = dsn

    def __str__(self) -> str:
        return self.dsn

    def __repr__(self) -> str:
        return f"<DatabaseConfig dsn={self.dsn}>"


class ConfigNode:
    """
    A configuration node for the bot.

    Attributes
    ----------
    bot : `BotConfig`
        The bot configuration.
    database : `DatabaseConfig`
        The database configuration.
    """

    def __init__(self, bot: BotConfig, database: DatabaseConfig) -> None:
        self.BOT: BotConfig = bot
        self.DATABASE: DatabaseConfig = database

    @staticmethod
    def from_dict(data: dict[str, Any]) -> ConfigNode:
        bot_data = data.get("BOT", {})
        database_data = data.get("DATABASE", {})

        bot_config = BotConfig(
            token=bot_data.get("token", ""),
            debug=bot_data.get("debug", False),
            version=bot_data.get("version", ""),
            exception_webhook=bot_data.get("exception_webhook", ""),
            owner_id=bot_data.get("owner_id", 0),
        )

        database_config = DatabaseConfig(
            dsn=database_data.get("dsn", ""),
        )

        return ConfigNode(bot=bot_config, database=database_config)


def load_config(file_path: Path) -> ConfigNode:
    """
    Load the configuration from the given file path.

    Parameters
    ----------
    file_path : `Path`
        The path to the configuration file [toml].
    """
    try:
        with open(file_path, "r") as fp:
            data = toml.load(fp)
            return ConfigNode.from_dict(data)
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file {file_path} not found.")
    except toml.TomlDecodeError:
        raise RuntimeError(f"Error decoding TOML file {file_path}.")


# Try to load the config.toml file ->
# IF failed to load raise a RuntimeError
CONFIG: ConfigNode = load_config(Path("config.toml"))
