import asyncio
import logging

import discord

import core


discord.utils.setup_logging(level=logging.INFO)


def main() -> None:
    async def start() -> None:
        async with core.Bot() as bot:
            await bot.start(core.CONFIG["BOT"]["token"], reconnect=True)

    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
