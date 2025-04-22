import os

class Config:
    """
    Configuration class for the Flask application.
    """
    CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
    CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('DISCORD_REDIRECT_URI')
    AUTHORIZATION_BASE_URL = os.getenv('AUTHORIZATION_BASE_URL')
    TOKEN_URL = os.getenv('TOKEN_URL')
    SCOPE = os.getenv('SCOPE').split(',')

config = Config()