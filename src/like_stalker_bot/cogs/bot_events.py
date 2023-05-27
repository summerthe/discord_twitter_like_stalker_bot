import discord
from discord.ext import bridge, commands
from discord.ext.commands.errors import MissingRequiredArgument

from ..config import Config


class BotEvents(commands.Cog):
    def __init__(self, bot: bridge.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Send bot is ready message on developer's discord channel."""
        await self.bot.get_channel(Config.bot_developer_channel).send(
            "Bot is online.",
        )

    @commands.Cog.listener()
    async def on_command_error(
        self,
        ctx: discord.ApplicationContext,
        error: discord.DiscordException,
    ):
        """Global command event handler.

        Parameters
        ----------
        ctx : discord.ApplicationContext
        error : discord.DiscordException

        Raises
        ------
        error
        """
        if isinstance(error, MissingRequiredArgument):
            # MissingRequiredArgument argument can occur from prefix commands.
            error_s = f"{error} Rerun command with the value, or type `!help {ctx.command}` for help."
            embed = discord.Embed(
                title="Missing argument",
                color=discord.Color.blurple(),
            )
            embed.description = error_s
            await ctx.send(embed=embed)
        else:
            raise error  # Here we raise other errors to ensure they aren't ignored


def setup(bot: bridge.Bot):
    bot.add_cog(BotEvents(bot))
