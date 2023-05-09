from typing import Optional

from sqlalchemy.orm import Session

from microservices.models.matching_room import MatchingRoom
from microservices.models.mr_liked_hated_member import MR_Liked_Hated_Member
from microservices.models.mr_member import MR_Member
from microservices.models.user import User


class CRUDLikedHatedMember:
    def get_by_email(db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_matching_room(db: Session, *, room_id: str):
        return db.query(MatchingRoom).filter(MatchingRoom.room_id == room_id).first()

    def get_member_in_matching_room(db: Session, *, room_uuid: str):
        return db.query(MR_Member).filter(MR_Member.room_uuid == room_uuid).all()

    def get_mr_user_pref_in_matching_room(db: Session, *, room_uuid: str):
        return (
            db.query(MR_Liked_Hated_Member)
            .filter(MR_Liked_Hated_Member.room_uuid == room_uuid)
            .all()
        )
