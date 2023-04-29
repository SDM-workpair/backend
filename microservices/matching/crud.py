from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User


class CRUDLikedHatedMember:
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
