import os
from typing import Union

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from loguru import logger
from pydantic import ValidationError
from sqlalchemy.orm import Session

# from fastapi_profiler import PyInstrumentProfilerMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app import crud, schemas
from app.core import security
from app.core.config import settings
from app.notifier import Notifier
from app.routers import deps
from app.routers.api_v1.api import api_router
from app.utils import get_tw_time

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
logger.info(f"Current env: {settings.ENV}")
if os.environ.get("ENV") == "dev":
    pass
    # app.add_middleware(
    #     PyInstrumentProfilerMiddleware,
    #     server_app=app,  # Required to output the profile on server shutdown
    #     profiler_output_type="html",
    #     is_print_each_request=False,  # Set to True to show request profile on
    #     # stdout on each request
    #     open_in_browser=False,  # Set to true to open your web-browser automatically
    #     # when the server shuts down
    #     html_file_name="./test/backend_profile.html",  # Filename for output
    # )

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


@app.websocket("/ws/{token}")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
    db: Session = Depends(deps.get_db),
):
    print("token >>> ", token)
    # decode token to get user email (email for notifier.setup())
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{e}",
        )
    print("payload >>> ", payload)
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=204, detail="User not found")
    print("user email >>> ", user.email)
    print("user name >>> ", user.name)

    # connect notifier with websocket
    notifier = Notifier()
    await notifier.connect(websocket)
    print("notifier >>> ", notifier)
    if not notifier.is_ready:
        print("notifier is not ready. ready to set up notifier with user email.")
        await notifier.setup(queue_name=user.email, is_consumer=True)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"text from client >>>: {data} ^_^")
            await websocket.send_text(f"Message text from client was: {data}")
    except WebSocketDisconnect:
        notifier.remove(websocket)
