from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.core.config import settings
from app.routers.api_v1.api import api_router
from app.utils import get_tw_time
import app.core.scheduler.matching_event

app = FastAPI(
    title=settings.APP_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json)"
)

origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]


GOOGLE_SECRET_KEY = settings.GOOGLE_SECRET_KEY or None
if GOOGLE_SECRET_KEY is None:
    raise "Missing SECRET_KEY"
app.add_middleware(SessionMiddleware, secret_key=GOOGLE_SECRET_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/api/healthchecker")
def read_root():
    return {"msg": "Hello World"}


@app.get("/api/basicinfo")
def get_info():
    return {"app_name": settings.APP_NAME, "time": get_tw_time()}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/test-google-sso")
async def test_google_sso(request: Request):
    """
    To test google sso with google button
    """
    # user = request.session.get('user')
    # if user is not None:
    #     email = user['email']
    html = (
        # f'<pre>Email: {email}</pre><br>'
        # '<a href="/docs">documentation</a><br>'
        # '<a href="/logout">logout</a>'
        "<body>"
        '<script src="https://accounts.google.com/gsi/client" async defer></script>'
        '<div id="g_id_onload"'
        'data-client_id="768305533256-eg3ift96spolgtm69bo6r3423df13c73.apps.googleusercontent.com"'
        'data-callback="handleCallback"'
        'data-auto_prompt="false">'
        "</div>"
        '<div class="g_id_signin"'
        'data-type="standard"'
        'data-size="large"'
        'data-theme="outline"'
        'data-text="sign_in_with"'
        'data-shape="rectangular"'
        'data-logo_alignment="left">'
        "</div>"
        "<script>"
        "function handleCallback(response) {"
        'fetch("http://localhost:8000/api/v1/auth/sso-login", {'
        "method: 'POST',"
        "headers: {"
        "'Content-Type': 'application/json'"
        "},"
        "body: JSON.stringify({credential: response.credential})"
        "})"
        ".catch(error => {"
        "console.error('Error:', error);"
        "});"
        "}"
        "</script>"
        "</body>"
    )
    return HTMLResponse(html)
    # return HTMLResponse('<a href="/login">login</a>')
