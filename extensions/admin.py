from typing import Literal, Annotated

import discord
from discord.ext import commands
from numpy import number
from _typings import Context, BaseCog
from bot import FIFIBot
from discord import app_commands

from discord.app_commands import locale_str as _T

class Admin(BaseCog):
    def __init__(self, bot: FIFIBot = FIFIBot) -> None:
        super().__init__(bot=bot)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
        self,
        ctx: Context,
        guilds: commands.Greedy[discord.Object],
        spec: Literal["~", "*", "^"] | None = None,
    ) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @app_commands.command(name=_T("testing"),
                          description=_T("This is a teting command."))
    @app_commands.describe(number=_T("This is a number."))
    async def test(self, interaction: discord.Interaction, number: int = 20) -> None:
        """
        This is a test command

        Parameters
        ----------
        number: int
            The number to test

        Permissions
        ----------
            This is extra data.
        """
        await interaction.response.send_message(f"Hello {number}")





async def setup(bot: FIFIBot) -> None:
    await bot.add_cog(Admin())
