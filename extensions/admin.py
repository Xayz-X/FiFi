from typing import Literal

import discord
from discord.ext import commands
from typings import Context, BaseCog
from bot import FIFIBot


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


    @commands.command()
    @commands.is_owner()
    async def test(self, ctx: Context, number: int=20) -> None:
        query = """
        SELECT name FROM test_data WHERE id = $1;  
        """
        result = await ctx.db.fetchrow(query, number)
        await ctx.send(result)



async def setup(bot: FIFIBot) -> None:
    await bot.add_cog(Admin())
