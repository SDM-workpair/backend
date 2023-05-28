import uuid
from typing import List, Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.notification import Notification
from app.models.notification_template import NotificationTemplate
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationViewModel,
)


class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    def get_by_sender_uuid(
        self, db: Session, *, sender_uuid: UUID
    ) -> Optional[List[NotificationViewModel]]:
        notification_viewmodel_list = []
        notifications = (
            db.query(Notification).filter(Notification.sender_uuid == sender_uuid).all()
        )
        for notification in notifications:
            # create a viewmodel and stored needed value
            notifiactionViewModel = NotificationViewModel(
                receiver_uuid=notification.receiver_uuid,
                send_time=notification.send_time,
                content=notification.f_string,
                is_read=notification.is_read,
                group_id=notification.group_id,
            )
            notification_viewmodel_list.append(notifiactionViewModel)
        return notification_viewmodel_list

    def get_by_receiver_uuid(
        self, db: Session, *, receiver_uuid: UUID
    ) -> Optional[List[NotificationViewModel]]:
        notification_viewmodel_list = []
        notifications = (
            db.query(Notification)
            .filter(Notification.receiver_uuid == receiver_uuid)
            .all()
        )
        for notification in notifications:
            # create a viewmodel and stored needed value
            notifiactionViewModel = NotificationViewModel(
                receiver_uuid=notification.receiver_uuid,
                send_time=notification.send_time,
                content=notification.f_string,
                is_read=notification.is_read,
                group_id=notification.group_id,
            )
            notification_viewmodel_list.append(notifiactionViewModel)
        return notification_viewmodel_list

    def create(self, db: Session, *, obj_in: NotificationCreate) -> Notification:
        notification_obj = (
            db.query(NotificationTemplate)
            .filter(NotificationTemplate.template_uuid == obj_in.template_uuid)
            .first()
        )
        if notification_obj is None:
            raise ValueError(
                f"Fail to retrieve notification_template with template_uuid={obj_in.template_uuid}"
            )
        else:
            notification_text = notification_obj.text
        # loop to replace
        for idx, f in enumerate(obj_in.f_string.split(";")):
            notification_text = notification_text.replace("{" + str(idx) + "}", f)

        db_obj = Notification(
            notification_uuid=uuid.uuid4(),  # generate a uuid as notification_uuid
            receiver_uuid=obj_in.receiver_uuid,
            # sender_uuid=obj_in.sender_uuid,
            send_time=obj_in.send_time,
            template_uuid=obj_in.template_uuid,
            f_string=notification_text,
            group_id=obj_in.group_id,
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def set_notifications_read(self, db: Session, *, user_uuid: UUID) -> None:
        db.query(Notification).filter(Notification.receiver_uuid == user_uuid).update(
            {"is_read": True}
        )
        db.commit()


notification = CRUDNotification(Notification)
