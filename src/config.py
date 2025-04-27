import os

class Config:
    """
    Configuration class for the Flask application.
    """
    DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
    DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
    DISCORD_REDIRECT_URI = os.getenv('DISCORD_REDIRECT_URI')
    DISCORD_AUTHORIZATION_BASE_URL = os.getenv('DISCORD_AUTHORIZATION_BASE_URL')
    DISCORD_TOKEN_URL = os.getenv('DISCORD_TOKEN_URL')
    DISCORD_SCOPE =  " ".join(os.getenv('DISCORD_SCOPE').split(","))

config = Config()