from datetime import timedelta
from typing import Any

import loguru
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Request,
                     Response)
from fastapi.responses import JSONResponse, ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.routers import deps

# from google.oauth2 import id_token
# from google.auth.transport import requests


# from fastapi_sso.sso.google import GoogleSSO

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    response: Response,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        loguru.logger.info("Incorrect email or password")
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        loguru.logger.info("Inactive user")
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = security.create_access_token(
        user.user_uuid, expires_delta=access_token_expires
    )

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
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.user = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


# @router.post("/google-login/access-token", response_model=schemas.Token)
# def google_login_access_token(
#     response: Response,
#     db: Session = Depends(deps.get_db),
#     form_data: OAuth2PasswordRequestForm = Depends()
# ) -> Any:

#     """
#     已驗證google登入帳號，直接產生token
#     """
#     user = crud.user.get_by_email(db, email=form_data.username)
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

#     access_token = security.create_access_token(
#         user.user_uuid, expires_delta=access_token_expires
#     )

#     response.set_cookie(
#         "access_token",
#         access_token,
#         settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
#         settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
#         "/",
#         None,
#         False,
#         True,
#         "lax",
#     )

#     response.set_cookie(
#         "logged_in",
#         "True",
#         settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
#         settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
#         "/",
#         None,
#         False,
#         False,
#         "lax",
#     )
#     return {
#             "access_token": access_token,
#             "token_type": "bearer",
#     }
