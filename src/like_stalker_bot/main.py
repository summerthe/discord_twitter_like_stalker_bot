from .bot import LikeStalkerBot
from .config import Config
from .utility.log_util import setup_logging

# Setting loggin
setup_logging()
# Set bot
print(Config.guild_ids)
bot = LikeStalkerBot(debug_guilds=Config.guild_ids, command_prefix="!")
bot.run(Config.token)
