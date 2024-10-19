from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from bot import FIFIBot


__all__: tuple[str, ...] = ("Context",)


class Context(commands.Context["FIFIBot"]):

    @staticmethod
    def tick(opt: bool | None, label: str | None = None) -> str:
        lookup = {
            True: "✅",
            False: "❌",
            None: "❔",
        }

        emoji = lookup.get(opt, "❌")
        if label is not None:
            return f"{emoji}: {label}"

        return emoji

    async def prompt(self) -> None:
        """
        Not implemented yet.
        """
        ...
        
        
        