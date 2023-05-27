import asyncio

from discord.ext import bridge, commands

from ..likes_checher_api import LikesChecher


class LikesCheck(commands.Cog):
    def __init__(self, bot: bridge.Bot):
        self.bot = bot
        self.api = LikesChecher()

    @bridge.bridge_command()
    async def clear(self, ctx: bridge.BridgeContext):
        """Deleted past messages of this channel.

        Args:
            ctx (bridge.BridgeContext):
        """
        channel = ctx.channel
        # Add `defer` to add `bot is thinking msg` for long running tasks.
        await ctx.defer()
        messages = await channel.history(limit=None).flatten()

        for message in messages:
            await message.delete()

        await asyncio.sleep(2)  # Add a delay of 2 seconds

        if ctx.message:
            try:
                await ctx.message.delete()  # Delete the command message if it exists
            except Exception:
                pass

    @bridge.bridge_command()
    async def check(self, ctx: bridge.BridgeContext, twitter_post_url: str):
        """Checks if post is liked by user or not.

        ex. `!check
        https://twitter.com/buitengebieden/status/1662149568056762368`
        """
        # Add `defer` to add `bot is thinking msg` for long running tasks.
        await ctx.defer()
        message = self.api.check_post_is_liked(
            post_url=twitter_post_url,
        )
        await ctx.respond(message)


def setup(bot):
    bot.add_cog(LikesCheck(bot))
