import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from sqlalchemy import update

from app.crud.base import CRUDBase
from app.models.matching_room import MatchingRoom
from app.models.mr_member_tag import MR_Member_Tag
from app.schemas.mr_member_tag import MR_Member_Tag_Create, MR_Member_Tag_Update
from app import crud
import loguru


class CRUDMR_Member_Tag(CRUDBase[MR_Member_Tag, MR_Member_Tag_Create, MR_Member_Tag_Update]):

    def get_1st_self_tag_by_member_id(
            self, 
            db: Session, 
            *, 
            member_id: int) -> MR_Member_Tag:
        return (
            db.query(MR_Member_Tag).filter(MR_Member_Tag.member_id == member_id, MR_Member_Tag.is_self_tag == True).first()
        )

    def get_1st_find_tag_by_member_id(
            self, 
            db: Session, 
            *, 
            member_id: int) -> MR_Member_Tag:
        return (
            db.query(MR_Member_Tag).filter(MR_Member_Tag.member_id == member_id, MR_Member_Tag.is_find_tag == True).first()
        )    

    def create_tag(
            self, 
            db: Session, 
            *, 
            is_self_tag: Optional[bool],
            is_find_tag: Optional[bool],
            mr_member_tag_in: MR_Member_Tag_Create) -> MR_Member_Tag:
        # Get matching_room uuid
        matching_room_in = crud.matching_room.get_by_room_id(db=db, room_id=mr_member_tag_in.matching_room.room_id)

        # Remove duplicated self-tag 
        original_tag_text_list =  mr_member_tag_in.tag_text_list
        seen = set()
        tag_text_list = []
        for tag in original_tag_text_list:
            if tag not in seen:
                tag_text_list.append(tag)
                seen.add(tag)

        db_obj_list = []

        for tag in tag_text_list:
            # Check if tag already existed
            tag_existed = db.query(
                                MR_Member_Tag
                            ).filter(
                                MR_Member_Tag.member_id == mr_member_tag_in.mr_member.member_id,
                                MR_Member_Tag.tag_text == tag
                            ).first()
            
            if tag_existed:
                if is_self_tag:
                    # Update self-tag
                    tag_existed.is_self_tag = True
                    db.commit()
                elif is_find_tag:
                    # Update find-tag
                    tag_existed.is_find_tag = True
                    db.commit()
                db_obj_list.append(tag_existed)

            else:
                # Insert new tag
                db_obj = MR_Member_Tag(
                    member_id=mr_member_tag_in.mr_member.member_id,
                    tag_text=tag,
                    room_uuid=matching_room_in.room_uuid,
                    is_self_tag=is_self_tag,
                    is_find_tag=is_find_tag
                )
                db.add(db_obj)
                db.commit()
                db_obj_list.append(db_obj)
                db.refresh(db_obj)
            
        return [tag.tag_text for tag in db_obj_list]


mr_member_tag = CRUDMR_Member_Tag(MR_Member_Tag)
