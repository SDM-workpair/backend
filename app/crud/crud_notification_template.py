from typing import Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.notification_template import NotificationTemplate
from app.schemas.notification_template import (
    NotificationTemplateCreate,
    NotificationTemplateUpdate,
)


class CRUDNotificationTemplate(
    CRUDBase[
        NotificationTemplate, NotificationTemplateCreate, NotificationTemplateUpdate
    ]
):
    def get_by_template_uuid(
        self, db: Session, *, template_uuid: UUID
    ) -> Optional[NotificationTemplate]:
        notification_template = (
            db.query(NotificationTemplate)
            .filter(NotificationTemplate.template_uuid == template_uuid)
            .first()
        )
        return notification_template

    def get_by_template_id(
        self, db: Session, *, template_id: str
    ) -> Optional[NotificationTemplate]:
        notification_template = (
            db.query(NotificationTemplate)
            .filter(NotificationTemplate.template_id == template_id)
            .first()
        )
        return notification_template


notification_template = CRUDNotificationTemplate(NotificationTemplate)
