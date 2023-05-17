import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.matching_room import MatchingRoom
from app.models.mr_member import MR_Member
from app.schemas.matching_room import (
    MatchingRoomCreate,
    MatchingRoomReq,
    MatchingRoomUpdate,
    MatchingRoomWithMemberID,
)


class CRUDMatchingRoom(CRUDBase[MatchingRoom, MatchingRoomCreate, MatchingRoomUpdate]):
    # TODO: separate each function or one function with dynamic filter?
    def get_by_room_uuid(
        self, db: Session, *, room_uuid: UUID
    ) -> Optional[MatchingRoom]:
        return (
            db.query(MatchingRoom).filter(MatchingRoom.room_uuid == room_uuid).first()
        )

    def get_by_room_id(self, db: Session, *, room_id: str) -> Optional[MatchingRoom]:
        return db.query(MatchingRoom).filter(MatchingRoom.room_id == room_id).first()

    def search_with_user_and_name(
        self,
        db: Session,
        *,
        user_uuid: UUID = None,
        name: str = "",
        is_query_with_user: bool = True
    ) -> Optional[List[MatchingRoomWithMemberID]]:
        # only filter out not grouped matching rooms
        matching_rooms = db.query(MatchingRoom).filter(MatchingRoom.is_closed == False)
        result = []
        if name != "":
            matching_rooms = matching_rooms.filter(
                MatchingRoom.name.ilike("%{}%".format(name))
            )
        mr_members = db.query(MR_Member).filter(MR_Member.user_uuid == user_uuid)
        # return only matching rooms user already joined
        if is_query_with_user:
            matching_rooms = matching_rooms.filter(
                MatchingRoom.room_uuid.in_([x.room_uuid for x in mr_members])
            )
        # exclude matching rooms user already joined
        else:
            matching_rooms = matching_rooms.filter(
                MatchingRoom.room_uuid.notin_([x.room_uuid for x in mr_members])
            )

        for matching_room in matching_rooms:
            if is_query_with_user:
                var_member_id = (
                    mr_members.filter(MR_Member.room_uuid == matching_room.room_uuid)
                    .first()
                    .member_id
                )
            else:
                var_member_id = None

            matching_room_with_member_id = MatchingRoomWithMemberID(
                room_id=matching_room.room_id,
                name=matching_room.name,
                due_time=matching_room.due_time,
                min_member_num=matching_room.min_member_num,
                description=matching_room.description,
                is_forced_matching=matching_room.is_forced_matching,
                created_time=matching_room.created_time,
                member_id=var_member_id,
            )
            result.append(matching_room_with_member_id)
        return result

    # def get_participated_in_matching_room(self, db: Session, *, user_email: str) -> Optional[List[MatchingRoom]]:
    #     user = db.query(User).filter(User.email == user_email).first()
    #     mr_members = db.query(MR_Member).filter(MR_Member.user_uuid == user.user_uuid)
    #     return db.query(MatchingRoom).filter(MatchingRoom.room_uuid.in_([x.room_uuid for x in mr_members])).all()

    # def get_by_name_filtering(self, db: Session, *, name) -> Optional[List[MatchingRoom]]:
    #     return db.query(MatchingRoom).filter(MatchingRoom.name.like("%{}%".format(name))).all()

    def create(self, db: Session, *, obj_in: MatchingRoomReq) -> MatchingRoom:
        def generate_id():
            temp_id = str(uuid.uuid4())[0:6]
            is_existed = self.get_by_room_id(db, room_id=temp_id)
            return temp_id, is_existed

        new_id = generate_id()

        while new_id[1]:
            new_id = generate_id()

        db_obj = MatchingRoom(
            room_uuid=uuid.uuid4(),  # generate a uuid as room_uuid
            name=obj_in.name,
            room_id=new_id[0],
            due_time=obj_in.due_time,
            min_member_num=obj_in.min_member_num,
            description=obj_in.description,
            is_forced_matching=obj_in.is_forced_matching,
            created_time=datetime.now(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, db_obj: MatchingRoom, room_id: str):
        if room_id is not None or room_id != "":
            db_obj = self.get_by_room_id(room_id)
            db.delete(db_obj)
            db.commit()
        return True


matching_room = CRUDMatchingRoom(MatchingRoom)
