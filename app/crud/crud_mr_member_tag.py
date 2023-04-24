import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.matching_room import MatchingRoom
from app.models.mr_member_tag import MR_Member_Tag
from app.schemas.mr_member_tag import MR_Member_Tag_Create, MR_Member_Tag_Update
from app import crud
import loguru


class CRUDMR_Member_Tag(CRUDBase[MR_Member_Tag, MR_Member_Tag_Create, MR_Member_Tag_Update]):

    def create_tag(
            self, 
            db: Session, 
            *, 
            is_self_tag: bool,
            is_find_tag: bool,
            mr_member_tag_in: MR_Member_Tag_Create) -> MR_Member_Tag:
        # Get matching_room uuid
        matching_room_in = crud.matching_room.get_by_room_id(db=db, room_id=mr_member_tag_in.matching_room.room_id)

        # Remove duplicated self-tag 
        original_tag_text_list =  mr_member_tag_in.tag_text_list
        loguru.logger.info(original_tag_text_list)
        seen = set()
        tag_text_list = []
        for tag in original_tag_text_list:
            if tag not in seen:
                tag_text_list.append(tag)
                seen.add(tag)

        # tag_text_list = [x for x in original_tag_text_list if x in seen or seen.add(x)]
        loguru.logger.info(seen)
        loguru.logger.info(tag_text_list)

        db_obj_list = []

        for tag in tag_text_list:
            db_obj = MR_Member_Tag(
                member_id=mr_member_tag_in.mr_member.member_id,
                tag_text=tag,
                room_uuid=matching_room_in.room_uuid,
                is_self_tag=is_self_tag,
                is_find_tag=is_find_tag
            )
            db.add(db_obj)
            db.commit()
            loguru.logger.info(db_obj)
            db_obj_list.append(db_obj)
            db.refresh(db_obj)
            
        loguru.logger.info(db_obj_list)
        return db_obj_list


mr_member_tag = CRUDMR_Member_Tag(MR_Member_Tag)
