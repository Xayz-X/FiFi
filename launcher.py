import logging
import asyncio
import discord

from core import CONFIG
from bot import FIFIBot
from database import create_pool


# setup discord logging
discord.utils.setup_logging(level=logging.INFO)

# setup logging
_log: logging.Logger = logging.getLogger(__name__)


# main function to run the bot
def main() -> None:

    async def start() -> None:

        # First try to connect to the database and create pool of 20 connections. 
        # [By default command timeout is 300 seconds]
        try:
            pool = await create_pool(dsn=CONFIG.DATABASE.dsn)
            _log.info(f"Created Database Pool Successfully")
        except Exception as e:
            _log.error(f"Failed to create pool: {e}")
            return

        # Then try to start the bot.
        async with FIFIBot() as bot:
            bot.pool = pool
            await bot.start(CONFIG.BOT.token, reconnect=True)

    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
