import asyncio
import logging
import core
import discord
from bot import FIFIBot
from database import create_pool

discord.utils.setup_logging(level=logging.INFO)


_log: logging.Logger = logging.getLogger(__name__)


def main() -> None:

    async def start() -> None:
        try:
            pool = await create_pool(dsn=core.CONFIG["DATABASE"]["dsn"])
        except Exception as e:
            _log.error(f"Failed to create pool: {e}")
            return
        async with FIFIBot() as bot:
            bot.pool = pool
            await bot.start(core.CONFIG["BOT"]["token"], reconnect=True)

    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
