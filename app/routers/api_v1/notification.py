from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.routers import deps

router = APIRouter()


@router.get("/my-list", response_model=schemas.NotificationTextWithMessage)
def read_my_notifications(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve user's notifications.
    """
    try:
        notifications = crud.notification.get_by_receiver_uuid(
            db=db, receiver_uuid=current_user.user_uuid
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Fail to retrieve notification: {e}"
        )

    return {"message": "success", "data": notifications}


@router.get("/set-read", response_model=schemas.NotificationTextWithMessage)
def set_notification_read(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Set user's all notifications read.
    """
    crud.notification.set_notifications_read(db=db, user_uuid=current_user.user_uuid)
    return {"message": "success"}


@router.get("/my-list/polling", response_model=schemas.NotificationPollingMessage)
def polling_my_notification(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return numbers of new notification.
    """
    # TODO: retrieve new notification
    return {"message": "success", "data": 1}
