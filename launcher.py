import asyncio
import logging
from core import CONFIG
import discord
from bot import FIFIBot
from database import create_pool

discord.utils.setup_logging(level=logging.INFO)


_log: logging.Logger = logging.getLogger(__name__)


def main() -> None:

    async def start() -> None:
        try:
            pool = await create_pool(dsn=CONFIG.DATABASE.dsn)
            _log.info(f"Created Database Pool Successfully")
        except Exception as e:
            _log.error(f"Failed to create pool: {e}")
            return
        async with FIFIBot() as bot:
            bot.pool = pool
            await bot.start(CONFIG.BOT.token, reconnect=True)

    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
