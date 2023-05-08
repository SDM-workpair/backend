from typing import List, Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.gr_member import GR_Member
from app.models.group import Group
from app.models.mr_member import MR_Member
from app.models.user import User
from app.schemas.gr_member import GR_MemberCreate, GR_MemberUpdate


class CRUDGR_Member(CRUDBase[GR_Member, GR_MemberCreate, GR_MemberUpdate]):
    def get_by_group_uuid(
        self, db: Session, *, group_uuid: UUID
    ) -> Optional[GR_Member]:
        return db.query(GR_Member).filter(GR_Member.group_uuid == group_uuid).all()

    def get_by_group_id(self, db: Session, *, group_id: str) -> Optional[GR_Member]:
        group_uuid = ""
        group = db.query(Group).filter(Group.group_id == group_id).first()
        if group is not None:
            group_uuid = group.group_uuid
            return self.get_by_group_uuid(db, group_uuid=group_uuid)
        else:
            return []

    def get_all_members_by_group_id(
        self, db: Session, *, group_id: str
    ) -> Optional[List[User]]:
        gr_members = self.get_by_group_id(db, group_id=group_id)
        member_list = []
        for gr_member in gr_members:
            # use member_id to retrieve mr_member
            mr_member = (
                db.query(MR_Member)
                .filter(MR_Member.member_id == gr_member.member_id)
                .first()
            )
            if mr_member is None:
                raise ValueError(
                    f"Fail to retrieve mr_member with member_id={gr_member.member_id}"
                )
            else:
                member = (
                    db.query(User).filter(User.user_uuid == mr_member.user_uuid).first()
                )
                if member is not None:
                    member_list.append(member)
        return member_list

    def create(self, db: Session, *, obj_in: GR_MemberCreate) -> GR_Member:
        db_obj = GR_Member(
            member_id=obj_in.member_id,
            group_uuid=obj_in.group_uuid,
            join_time=obj_in.join_time,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_by_group_id(self, db: Session, *, group_id: str):
        if group_id is not None or group_id != "":
            db_objs = self.get_by_group_id(group_id)
            for db_obj in db_objs:
                db.delete(db_obj)
            db.commit()
        return True


gr_member = CRUDGR_Member(GR_Member)
