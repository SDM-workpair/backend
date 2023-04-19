from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.routers import deps

router = APIRouter()


@router.post("/my-list", response_model=schemas.NotificationTextWithMessage)
def read_my_notifications(
    user_in: schemas.User,
    db: Session = Depends(deps.get_db)  # ,
    # current_user: models.user = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve user's notifications.
    """
    #  先看user_email是否找得到user再去query matching room
    if user_in.email == "" or user_in.email is None:
        raise HTTPException(
            status_code=400,
            detail="Fail to retrieve user's notifications. Missing parameter: email.",
        )
    user = crud.user.get_by_email(db=db, email=user_in.email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Fail to find user with this email.",
        )
    notifications = crud.notification.get_by_receiver_uuid(
        db=db, receiver_uuid=user.user_uuid
    )

    return {"message": "success", "data": notifications}
