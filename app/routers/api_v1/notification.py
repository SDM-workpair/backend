from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.notifier import notify
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
    notifications = crud.notification.get_by_receiver_uuid(
        db=db, receiver_uuid=current_user.user_uuid
    )
    unread_num = len([x for x in notifications if x.is_read is False])

    return {"message": "success", "data": notifications, "unread_num": unread_num}


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


@router.post("/trigger_matching_event")
async def trigger_matching_event(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Trigger matching event and send notification into rabbitmq queue. (only for test)
    """
    # send_notification_to_rabbit_mq(db, group_members)
    # notification_send_object_1 = schemas.NotificationSendObjectModel(
    #     receiver_uuid="5f1e19a8-70a9-44b9-b026-1584c5df4f5a",
    #     sender_uuid="2be6b063-8914-42b6-9e8d-1bbe14317cc2",
    #     template_uuid="9c1dc87f-e938-4fa1-9900-9b4ebd5701da",
    #     f_string="配對結果111",
    # )
    # notification_send_object_2 = schemas.NotificationSendObjectModel(
    #     receiver_uuid="57d02352-e057-4878-a05e-70713badca56",
    #     sender_uuid="2be6b063-8914-42b6-9e8d-1bbe14317cc2",
    #     template_uuid="9c1dc87f-e938-4fa1-9900-9b4ebd5701da",
    #     f_string="配對結果111",
    # )
    notification_send_object_3 = schemas.NotificationSendObjectModel(
        receiver_uuid="70528b75-1ebc-4117-b3dc-c6127264fcff",
        sender_uuid="2be6b063-8914-42b6-9e8d-1bbe14317cc2",
        template_uuid="9c1dc87f-e938-4fa1-9900-9b4ebd5701da",
        f_string="配對結果111",
    )
    notification_send_object_4 = schemas.NotificationSendObjectModel(
        receiver_uuid="397d0336-3df4-4325-a1b3-cc4ef8e8e0ab",
        sender_uuid="2be6b063-8914-42b6-9e8d-1bbe14317cc2",
        template_uuid="9c1dc87f-e938-4fa1-9900-9b4ebd5701da",
        f_string="配對結果111",
    )
    # await notify(db, notification_send_object_1)
    # await notify(db, notification_send_object_2)
    await notify(db, notification_send_object_3)
    await notify(db, notification_send_object_4)
