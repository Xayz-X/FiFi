from __future__ import annotations

from asyncpg import Pool
from typing import TYPE_CHECKING

from ui import ConfirmationView
from discord.ext import commands
from discord import Embed
from aiohttp import ClientSession

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

    @property
    def session(self) -> ClientSession:
        """Get the bot web client session."""
        return self.bot.session

    @staticmethod
    def tick(opt: bool | None, label: str | None = None) -> str:
        """
        Get a tick emoji based on the boolean value.

        Parameters
        ----------
        opt : bool | None
            The boolean value to get the emoji for.
        label : str | None, optional
            The label to show along with the emoji, by default None

        Returns
        -------
        str
            The emoji with the label.
        """
        lookup = {
            True: "✅",
            False: "❌",
            None: "❔",
        }

        emoji = lookup.get(opt, "❌")
        if label is not None:
            return f"{emoji}: {label}"

        return emoji

    async def prompt(
        self,
        message: str | None = None,
        embed: Embed | None = None,
        *,
        timeout: float = 60.0,
        delete_after: bool = True,
        author_id: int | None = None,
    ) -> bool | None:
        """
        An interactive reaction confirmation prompt.

        Parameters
        -----------
        message: `str | None`
            The message to show along with the prompt.
        embed: `Embed | None`
            The embed to show along with the prompt.
        timeout: `float`
            How long to wait before returning.
        delete_after: `bool`
            Whether to delete the confirmation message after we're done.
        author_id: `int | None`
            The member who should respond to the prompt. Defaults to the author of the
            Context's message.

        Returns
        --------
        bool | None
            ``True`` if explicit confirm,
            ``False`` if explicit deny,
            ``None`` if deny due to timeout
        """

        author_id = author_id or self.author.id
        view = ConfirmationView(
            timeout=timeout,
            delete_after=delete_after,
            author_id=author_id,
        )
        view.message = await self.send(
            content=message, embed=embed, view=view, ephemeral=delete_after
        )
        await view.wait()
        return view.value
