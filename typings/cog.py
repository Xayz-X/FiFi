from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from bot import FIFIBot

__all__: tuple[str, ...] = ("BaseCog",)


class BaseCog(commands.Cog):
    def __init__(self, bot: FIFIBot) -> None:
        self.bot: FIFIBot = bot



