import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.matching_room import MatchingRoom
from app.models.mr_member import MR_Member
from app.schemas.mr_member import MR_Member_Create, MR_Member_Update, MR_Member_Req
import loguru


class CRUDMR_Member(CRUDBase[MR_Member, MR_Member_Create, MR_Member_Update]):
    def get_by_room_uuid_and_user_uuid(
            self, db: Session, *, room_uuid: str, user_uuid: str
        ) -> Optional[MR_Member]:
        return (
            db.query(MR_Member).filter(MR_Member.room_uuid == room_uuid, MR_Member.user_uuid == user_uuid).first()
        )
    
    def get_by_member_id(
            self, db: Session, *, member_id: str
    ) -> Optional[MR_Member]:
        return (
            db.query(MR_Member).filter(MR_Member.member_id == member_id).first()
        )

    def create(self, db: Session, *, room_uuid: str, user_uuid: str) -> MR_Member:
        db_obj = MR_Member(
            user_uuid=user_uuid,
            room_uuid=room_uuid,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj

    def delete(self, db: Session, *, db_obj: MR_Member):
        db.delete(db_obj)
        db.commit()
        return True


mr_member = CRUDMR_Member(MR_Member)
