from pathlib import Path

import discord
from discord.ext import bridge

from .utility.helper import LikeStalkerHelpCommand


class LikeStalkerBot(bridge.Bot):
    """Bot to check if post is liked by user or not related application
    commands.

    Subclassed to enable default intents and message_content. Subclassed
    from `bridge.Bot` instead of `discord.Bot` to generate slash and
    application commands both for same function. Making `cogs`to being
    loaded from cogs directory.
    """

    def __init__(self, description=None, *args, **options):
        # Set intents
        intents = discord.Intents.default()
        intents.message_content = True
        options["intents"] = intents
        options["help_command"] = LikeStalkerHelpCommand()
        super().__init__(description=description, *args, **options)
        # List and log cogs, excluding file which start with _(underscode).
        cogs_list = [
            _path.stem for _path in Path("like_stalker_bot/cogs").glob("[!_]*.py")
        ]
        for cog in cogs_list:
            self.load_extension(f"like_stalker_bot.cogs.{cog}")
