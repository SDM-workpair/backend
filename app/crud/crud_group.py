import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.gr_member import GR_Member
from app.models.group import Group
from app.models.user import User
from app.schemas.group import GroupCreate, GroupUpdate


class CRUDGroup(CRUDBase[Group, GroupCreate, GroupUpdate]):
    # TODO: separate each function or one function with dynamic filter?
    def get_by_group_uuid(self, db: Session, *, group_uuid: UUID) -> Optional[Group]:
        return db.query(Group).filter(Group.group_uuid == group_uuid).first()

    def get_by_group_id(self, db: Session, *, group_id: str) -> Optional[Group]:
        return db.query(Group).filter(Group.group_id == group_id).first()

    def search_with_user_and_name(
        self, db: Session, *, user_uuid: UUID = None, name: str = ""
    ) -> Optional[List[Group]]:
        groups = db.query(Group)
        # filter out matching rooms for user first
        if user_uuid:
            gr_members = db.query(GR_Member).filter(GR_Member.user_uuid == user_uuid)
            groups = groups.filter(
                Group.group_uuid.in_([x.group_uuid for x in gr_members])
            )
        if name != "":
            groups = groups.filter(Group.name.ilike("%{}%".format(name)))
        return groups.all()

    def create(self, db: Session, *, obj_in: GroupCreate) -> Group:
        db_obj = Group(
            group_uuid=uuid.uuid4(),  # generate a uuid as group_uuid
            name=obj_in.name,
            group_id=obj_in.group_id,
            room_uuid=obj_in.room_uuid,
            created_time=datetime.now(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, db_obj: Group, group_id: str):
        if group_id is not None or group_id != "":
            db_obj = self.get_by_group_id(group_id)
            db.delete(db_obj)
            db.commit()
        return True


group = CRUDGroup(Group)
