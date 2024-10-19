import logging
import sys
import aiohttp
import asyncpg
from typing_extensions import Self

import discord
from discord.ext import commands

from typings import Context
from core import CONFIG
from translations import TreeTranslator


_log: logging.Logger = logging.getLogger(__name__)


class FIFIBot(commands.Bot):

    pool: asyncpg.Pool = None

    def __init__(self) -> None:
        ua: str = (
            f"FiFi Bot/{CONFIG.BOT.version}, Python/{sys.version}, Discord.py/{discord.__version__}"
        )
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers={"User-Agent": ua}
        )
        self.debug: bool = CONFIG.BOT.debug

        intents: discord.Intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(
            command_prefix=["f! ", "?"], intents=intents, case_insensitive=True
        )

    async def get_context(
        self, origin: discord.Message | discord.Interaction[Self]
    ) -> Context:
        return await super().get_context(origin, cls=Context)

    async def setup_hook(self) -> None:

        await self.tree.set_translator(
            TreeTranslator()
        )  # sets the custom translator for the bot

        await self.load_extension("jishaku")
        await self.load_extension("extensions")

    async def on_ready(self) -> None:
        _log.info(f"Logged in as: {self.user}")

    async def close(self) -> None:
        await self.session.close()
        return await super().close()
