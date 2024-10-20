from __future__ import annotations

import io
from asyncpg import Pool
from aiohttp import ClientSession
from typing import TYPE_CHECKING, Any

import discord
from discord.ext import commands

from ui import ConfirmationView
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
        opt : `bool | None`
            The boolean value to get the emoji for.
        label : `str | None`, optional
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
        message: str = "",
        embed: discord.Embed | None = None,
        *,
        timeout: float = 60.0,
        delete_after: bool = True,
        author_id: int | None = None,
    ) -> bool | None:
        """
        An interactive reaction confirmation prompt.

        Parameters
        -----------
        message: `str`
            The message to show along with the prompt.
        embed: `discord.Embed | None`
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
            content=message,
            embed=embed,
            view=view,
            ephemeral=delete_after,  # content cannot be none so we set the defualt value to empty string -> ""
        )
        await view.wait()
        return view.value

    async def safe_send(
        self, content: str, *, escape_mentions: bool = True, **kwargs
    ) -> discord.Message:
        """
        Safe send allow to send big message which is over 2000 characters.

        Parameters
        ----------
        content: `str`
            The content to send.
        escape_mentions: `bool`
            Whether to escape mentions like @username.
        """
        if escape_mentions:
            content = discord.utils.escape_mentions(content)

        if len(content) > 2000:
            fp = io.BytesIO(content.encode())
            kwargs.pop("file", None)
            return await self.send(
                file=discord.File(fp, filename="message_too_long.txt"), **kwargs
            )
        else:
            return await self.send(content)

    async def show_help(self, command: Any | None = None) -> None:
        """
        Shows the help command for the specified command if given.
        If no command is given, then it'll show help for the current command.

        Parameters
        ----------
        command: `Any | None`
            The command to show help for.
        """

        cmd = self.bot.get_command("help")
        command = command or self.command.qualified_name
        await self.invoke(cmd, command=command)
