from flask import Flask, redirect, request, session
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv
import requests
from flasgger import Swagger
from config import config

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Swagger configuration
app.config['SWAGGER'] = {
    'title': 'Discord Login API',
    'uiversion': 3
}

swagger = Swagger(app)


@app.get('/login')
def login():
    """
    Redirects user to Discord for authorization.
    ---
    responses:
      302:
        description: Redirect to Discord's authorization page.
    """
    discord = OAuth2Session(config.CLIENT_ID, redirect_uri=config.REDIRECT_URI, scope=config.SCOPE)
    authorization_url, state = discord.authorization_url(config.AUTHORIZATION_BASE_URL)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.get("/callback/")
def callback():
    """
    Handles the callback from Discord, exchanges the code for an access token.
    ---
    parameters:
      - name: code
        in: query
        type: string
        required: true
        description: The authorization code received from Discord.
      - name: state
        in: query
        type: string
        required: true
        description: The state returned by Discord.
    responses:
      200:
        description: Returns the access token and other data.
    """
    code = request.args.get('code')
    state = request.args.get('state')
    data = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': config.REDIRECT_URI
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    r = requests.post(config.TOKEN_URL, data=data, headers=headers, auth=(config.CLIENT_ID, config.CLIENT_SECRET))
    r.raise_for_status()
    return r.json()


@app.get('/getuserinfo/')
def get_userinfo():
    """
    Retrieves user information from Discord using the access token.
    ---
    parameters:
      - name: access_token
        in: query
        type: string
        required: true
        description: The access token obtained from the callback.
    responses:
      200:
        description: Returns the user information.
    """
    access_token = request.args.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
    r.raise_for_status()
    user = r.json()
    user['avatar'] = get_user_avatar(user)
    return user



def get_user_avatar(user):
    """Get user profile image"""
    if user['avatar'] is None:
        return "https://cdn.discordapp.com/embed/avatars/0.png"
    return f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png?size=1024"
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)