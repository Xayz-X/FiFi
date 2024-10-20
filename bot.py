import logging
import sys
import aiohttp
import asyncpg

import discord
from discord.ext import commands

from typings import Context
from core import CONFIG
from translations import TreeTranslator


_log: logging.Logger = logging.getLogger(__name__)


class FIFIBot(commands.Bot):

    pool: asyncpg.Pool

    def __init__(self) -> None:
        ua: str = (
            f"FiFi Bot/{CONFIG.BOT.version}, Python/{sys.version}, Discord.py/{discord.__version__}"  # user agent string
        )

        self.session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers={"User-Agent": ua}
        )  # a aiohttp web client session -> Only close when bot is closed.

        self.debug: bool = CONFIG.BOT.debug  # debug mode of the bot
        self.uptime = discord.utils.utcnow()  # uptime of the bot

        intents: discord.Intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix=["f!", "?"],
            intents=intents,
            case_insensitive=True,
            strip_after_prefix=True,
        )

    async def get_context(
        self, origin: discord.Interaction | discord.Message, /, *, cls=Context
    ) -> Context:
        # get the context of the message or interaction
        return await super().get_context(origin, cls=cls)


    async def setup_hook(self) -> None:
        # setup function only call once when bot is ready
        await self.tree.set_translator(TreeTranslator())
        await self.load_extension("jishaku")
        await self.load_extension("extensions")

    async def on_ready(self) -> None:
        _log.info(f"Logged in as: {self.user}")

    async def close(self) -> None:
        # close the session when bot is closing
        await self.session.close()
        _log.info("Closed Bot Session")
        return await super().close()

    # async def start(self) -> None:
    #     await super().start(CONFIG.BOT.token, reconnect=True)
