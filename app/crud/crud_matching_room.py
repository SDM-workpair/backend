import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.matching_room import MatchingRoom
from app.models.mr_member import MR_Member
from app.schemas.matching_room import MatchingRoomCreate, MatchingRoomUpdate, MatchingRoomReq
import loguru


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
        self, db: Session, *, user_uuid: UUID = None, name: str = ""
    ) -> Optional[List[MatchingRoom]]:
        matching_rooms = db.query(MatchingRoom)
        # filter out matching rooms for user first
        if user_uuid:
            mr_members = db.query(MR_Member).filter(MR_Member.user_uuid == user_uuid)
            print("mr_members >>> ", mr_members)
            matching_rooms = matching_rooms.filter(
                MatchingRoom.room_uuid.in_([x.room_uuid for x in mr_members])
            )
            print("matching_rooms >>> ", matching_rooms)
        if name != "":
            matching_rooms = matching_rooms.filter(
                MatchingRoom.name.ilike("%{}%".format(name))
            )
        return matching_rooms.all()

    # def get_participated_in_matching_room(self, db: Session, *, user_email: str) -> Optional[List[MatchingRoom]]:
    #     user = db.query(User).filter(User.email == user_email).first()
    #     mr_members = db.query(MR_Member).filter(MR_Member.user_uuid == user.user_uuid)
    #     return db.query(MatchingRoom).filter(MatchingRoom.room_uuid.in_([x.room_uuid for x in mr_members])).all()

    # def get_by_name_filtering(self, db: Session, *, name) -> Optional[List[MatchingRoom]]:
    #     return db.query(MatchingRoom).filter(MatchingRoom.name.like("%{}%".format(name))).all()

    def create(self, db: Session, *, obj_in: MatchingRoomReq) -> MatchingRoom:

        def generate_id():
            temp_id = str(uuid.uuid4())[0:6]
            is_existed = self.get_by_room_id(db, room_id = temp_id)
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
