from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
from config import config
import uvicorn
from fastapi.responses import RedirectResponse
import requests
import httpx

load_dotenv()
app = FastAPI()
app.secret_key = os.urandom(24)



@app.get('/login')
def login():
    """
    Redirects user to Discord for authorization.
    ---
    responses:
      302:
        description: Redirect to Discord's authorization page.
    """
    discord_auth_url = (
            f"https://discord.com/api/oauth2/authorize"
            f"?client_id={config.DISCORD_CLIENT_ID}"
            f"&redirect_uri={config.DISCORD_REDIRECT_URI}"
            f"&response_type=code"
            f"&scope={config.DISCORD_SCOPE}"
        )

    return RedirectResponse(url=discord_auth_url)


@app.get("/callback/")
async def callback(request: Request, code: str = None, state: str = None):
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
    try:

        data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': config.DISCORD_REDIRECT_URI
        }
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(config.DISCORD_TOKEN_URL, data=data, headers=headers, auth=(config.DISCORD_CLIENT_ID, config.DISCORD_CLIENT_SECRET))
            

            access_token = response.json().get('access_token')
            return await __get_user_info(access_token)
    except Exception as e:
        return {"error": str(e)}
        

async def __get_user_info(access_token):
    """
    Fetches user information from Discord using the access token.
    ---
    parameters:
      - name: access_token
        in: query
        type: string
        required: true
        description: The access token received from Discord.
    responses:
      200:
        description: Returns user information.
    """
    try:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get('https://discord.com/api/v10/users/@me', headers=headers)
            response.raise_for_status()
            user = response.json()
            user['avatar'] = __get_user_avatar(user)
            return user
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"}
    except httpx.RequestError as e:
        return {"error": f"Request error occurred: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}



def __get_user_avatar(user):
    """Get user profile image"""
    if user['avatar'] is None:
        return "https://cdn.discordapp.com/embed/avatars/0.png"
    return f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png?size=1024"
    

if __name__ == "__main__":
    uvicorn.run("app:app", port=5000, reload=True)
