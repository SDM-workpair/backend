from typing import Optional

from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.models.tag import Tag
from app.schemas.tag import Tag_Create, Tag_Update
from uuid import UUID

class CRUD_Tag(
    CRUDBase[Tag, Tag_Create, Tag_Update]
):
    def get_by_room_uuid_and_tag_text(self, db: Session, *, room_uuid: UUID, tag_text: str) -> Tag:
        tag_text = tag_text.upper()
        return( 
            db.query(Tag)
            .filter(
                Tag.room_uuid == room_uuid, Tag.tag_text == tag_text
            )
            .first())
    
    def create(self, db: Session, *, tag_in: Tag_Create) -> Tag:
        # Get matching_room uuid
        matching_room_in = crud.matching_room.get_by_room_id(
            db=db, room_id=tag_in.matching_room.room_id
        )

        # Check if tag in this matching room already existed
        tag_existed = tag.get_by_room_uuid_and_tag_text(
            db=db, room_uuid=matching_room_in.room_uuid, tag_text=tag_in.tag_text
        )

        # Y: Update mentioned num
        if tag_existed:
            tag_existed.mentioned_num += 1
            db.commit()
            return tag_existed
        # N: Add new tag
        else:
            tag_text = tag_in.tag_text.upper()
            db_obj = Tag(
                tag_text = tag_text,
                room_uuid = matching_room_in.room_uuid,
                mentioned_num = 1,
            )
            db.add(db_obj)
            db.commit()
            return db_obj


tag = CRUD_Tag(Tag)
