from __future__ import annotations

from asyncpg import Pool
from typing import TYPE_CHECKING

from discord.ext import commands


from database import DatabaseProtocol

if TYPE_CHECKING:
    from bot import FIFIBot


__all__: tuple[str, ...] = ("Context",)


class Context(commands.Context["FIFIBot"]):

    bot: FIFIBot

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pool: Pool = self.bot.pool

    @property
    def db(self) -> DatabaseProtocol:
        """A database connection pool."""
        return self.pool

    @staticmethod
    def tick(opt: bool | None, label: str | None = None) -> str:
        lookup = {
            True: "✅",
            False: "❌",
            None: "❔",
        }

        emoji = lookup.get(opt, "❌")
        if label is not None:
            return f"{emoji}: {label}"

        return emoji

    async def prompt(self) -> None:
        """
        Not implemented yet.
        """
        ...
