from __future__ import annotations

import logging
import discord
import traceback
from datetime import datetime
from collections import defaultdict
from typing import (
    TYPE_CHECKING,
    Any,
    Generator,
    TypeAlias,
    DefaultDict,
)


if TYPE_CHECKING:
    from bot import FIFIBot
    from context import Context
    from core import CONFIG


Traceback: TypeAlias = dict[str, Any]


_log: logging.Logger = logging.getLogger(__name__)


__all__: tuple[str, ...] = ("PacketManager",)


class PacketManager:
    """An extension to the error handler that keeps track of errors and sends them to a webhook.

    Attributes
    ----------
    bot: FIFIBot
        The bot instance.
    errors: DefaultDict[str, list[Traceback]]
        A mapping of trace backs to their error information.
    """

    __slots__: tuple[str, ...] = (
        "bot",
        "cooldown",
        "_lock",
        "_most_recent",
        "errors",
        "_code_blocker",
        "_error_webhook",
    )

    def __init__(self, bot: FIFIBot) -> None:
        self.bot: FIFIBot = bot

        self.errors: DefaultDict[str, list[Traceback]] = defaultdict(list)

        self._code_blocker: str = "```py\n{}```"
        self._error_webhook: discord.Webhook = discord.Webhook.from_url(
            CONFIG.BOT.exception_webhook, session=bot.session, bot_token=bot.http.token
        )

    def _yield_code_chunks(
        self, iterable: str, *, chunks: int = 2000
    ) -> Generator[str, None, None]:
        code_blocker_size: int = len(self._code_blocker) - 2

        for i in range(0, len(iterable), chunks - code_blocker_size):
            yield self._code_blocker.format(
                iterable[i : i + chunks - code_blocker_size]
            )

    async def _release_error(self, traceback_str: str, packet: Traceback) -> None:
        _log.error("Releasing error to log", exc_info=packet["exception"])

        embed = discord.Embed(
            title=f'An error has occurred in {packet["command"]}',
            timestamp=packet["time"],
        )
        embed.add_field(
            name="Metadata",
            value="\n".join([f"**{k.title()}**: {v}" for k, v in packet.items()]),
        )

        kwargs: dict[str, Any] = {}
        if self.bot.user:
            kwargs["username"] = self.bot.user.display_name
            kwargs["avatar_url"] = self.bot.user.display_avatar.url

            embed.set_author(
                name=str(self.bot.user), icon_url=self.bot.user.display_avatar.url
            )

        webhook = self._error_webhook
        if webhook.is_partial():
            self._error_webhook = webhook = await self._error_webhook.fetch()

        code_chunks = list(self._yield_code_chunks(traceback_str))

        embed.description = code_chunks.pop(0)
        await webhook.send(embed=embed, **kwargs)

        embeds: list[discord.Embed] = []
        for entry in code_chunks:
            embed = discord.Embed(description=entry)
            if self.bot.user:
                embed.set_author(
                    name=str(self.bot.user), icon_url=self.bot.user.display_avatar.url
                )

            embeds.append(embed)

            if len(embeds) == 10:
                await webhook.send(embeds=embeds, **kwargs)
                embeds = []

        if embeds:
            await webhook.send(embeds=embeds, **kwargs)

    async def add_error(
        self,
        *,
        error: BaseException,
        target: Context | discord.Interaction[FIFIBot] | None = None,
        event_name: str | None = None,
    ) -> None:
        """
        Add an error to the error manager. This will handle all cooldowns and internal cache management.

        Parameters
        ----------
        error: `BaseException`
            The error to add.
        target: `Context` | `discord.Interaction[FIFIBot]` | `None`
            The invocation context of the error, if any.
        event_name: `str` | `None`
            The name of the event that the error occurred in, if any.
        """
        _log.info(f"Adding error {str(error)} to log.")

        created: datetime.datetime = discord.utils.utcnow()
        author: discord.Member | discord.User | None = None

        if target is not None:
            if isinstance(target, Context):
                created = target.message.created_at
                author = target.author
            else:
                author = target.user
                created = target.created_at

        packet: Traceback = {
            "exception": error,
            "time": created,
            "command": "no command",
        }

        if event_name:
            packet["event_name"] = event_name

        if target:
            addons: dict[str, str | None] = {
                "command": target.command and target.command.qualified_name,
                "author": author and f"<@{author.id}> ({author.id})",
                "guild": target.guild and f"{target.guild.name} ({target.guild.id})",
                "channel": target.channel
                and f"<#{target.channel.id}> ({target.channel.id})",
            }
            packet.update(addons)

        traceback_string = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        self.errors[traceback_string].append(packet)

        await self._release_error(traceback_string, packet)
