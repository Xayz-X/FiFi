import logging
import pathlib
from discord.ext import commands
from bot import FIFIBot

logger: logging.Logger = logging.getLogger(__name__)


async def setup(bot: FIFIBot) -> None:
    NO_LOAD: list[str] = [".test"]
    extensions: list[str] = [
        f".{f.stem}" for f in pathlib.Path("extensions").glob("*[a-zA-Z].py")
    ]
    loaded: list[str] = []

    for extension in extensions:
        if bot.debug and extension in NO_LOAD:
            logger.info(
                f"Skipped loading: {extension} as bot is currently in debug mode."
            )
            continue

        try:
            await bot.load_extension(extension, package="extensions")
        except Exception as e:
            logger.error(f"Unable to load extension: {extension} > {e}")
        else:
            loaded.append(f"extensions{extension}")

    logger.info(f"Loaded the following extensions: {loaded}")


async def teardown(bot: FIFIBot) -> None:
    extensions: list[str] = [
        f".{f.stem}" for f in pathlib.Path("extensions").glob("*[a-zA-Z].py")
    ]

    for extension in extensions:
        try:
            await bot.unload_extension(extension, package="extensions")
        except commands.ExtensionNotLoaded:
            pass
