from .utility.env_util import set_env

env = set_env()


class Config:
    # Twitter API
    twitter_consumer_key = env("TWITTER_CONSUMER_KEY")
    twitter_consumer_secret = env("TWITTER_CONSUMER_SECRET")
    twitter_access_token = env("TWITTER_ACCESS_TOKEN")
    twitter_access_token_secret = env("TWITTER_ACCESS_TOKEN_SECRET")
    user_screen_name = env("USER_SCREEN_NAME")

    # Discord
    guild_ids = env.list("GUILD_IDS")
    bot_developer_channel = env.int("BOT_DEVELOPER_CHANNEL", int)
    token = env("TOKEN")
