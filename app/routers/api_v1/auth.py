from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.encoders import jsonable_encoder
from google.auth.transport import requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import crud
from app.core import security
from app.core.config import settings
from app.routers import deps
from app.schemas.user import UserCreate

# Create the auth app
router = APIRouter()


@router.post("/sso-login")
def google_auth(
    request: Request,
    response: Response,
    db: Session = Depends(deps.get_db),
    credential: str = Form(...),
) -> Any:
    """
    Google credential decode and authentication
    """
    # Supplied by g_id_onload
    tokenid = credential
    try:
        idinfo = id_token.verify_oauth2_token(
            tokenid,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=5,
        )

        # # 檢查此google帳號是否已建立帳號
        user = crud.user.get_by_email(db, email=idinfo["email"])

        # 帳號尚未建立，create user
        if not user:
            user_in = UserCreate(
                **{
                    "email": idinfo["email"],
                    "name": idinfo["name"],
                    "image": idinfo["picture"],
                    "is_google_sso": True,
                }
            )
            crud.user.create(db, obj_in=user_in)

        # 帳號已建立，取得access token
        user = crud.user.get_by_email(db, email=idinfo["email"])
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            user.user_uuid, expires_delta=access_token_expires
        )
        request.session["user"] = jsonable_encoder(user)
        request.session["authorization"] = access_token
        response.set_cookie(
            "access_token",
            access_token,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "/",
            None,
            False,
            True,
            "lax",
        )

        response.set_cookie(
            "logged_in",
            "True",
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "/",
            None,
            False,
            False,
            "lax",
        )
        access_token = {
            "access_token": access_token,
            "token_type": "bearer",
        }

        # 回傳 Matching room list

        return
    except ValueError:
        # Invalid token
        return JSONResponse(
            status_code=401,
            content={"message": "Unauthorized", "data": None},
        )
