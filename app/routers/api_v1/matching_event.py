from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.routers import deps
import loguru
import json
# from app.core.scheduler import matching_event

router = APIRouter()

# TODO
@router.post("/")
# , response_model=schemas.Group
def initiate_matching_event(
    *,
    db: Session = Depends(deps.get_db),
    matching_room_in: schemas.MatchingRoomBase,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Initiate matching event.
    """
    matching_room = crud.matching_room.get_by_room_id(db=db, room_id=matching_room_in.room_id)
    if not matching_room:
        raise HTTPException(
            status_code=400,
            detail="Matching room with this room_id does not exist in this system.",
        )
    # result = matching_event(matching_room)

    result = [[1, 2],[3, 4, 5],[6, 7]] #要是int

    # 可能要寫到一個method裡面(scheduler也會call)
    group_list = []
    group_id = 0
    for group in result:
        # Create Group
        group_id += 1
        new_group_schema = schemas.GroupCreate(
            name=matching_room.room_id + "_" + str(group_id),
            group_id=str(group_id),
            room_uuid=matching_room.room_uuid
        )
        new_group = crud.group.create(db=db, obj_in=new_group_schema)

        gr_mem_list = []
        for gr_member in group:
            # Create GR_member
            new_gr_mem_schema = schemas.GR_MemberCreate(
                member_id=gr_member,
                group_uuid=new_group.group_uuid,
                join_time=new_group.create_time
            )
            new_gr_mem = crud.gr_member.create(db=db, obj_in=new_gr_mem_schema)
            # Call notification method for every Group Mem
            gr_user = crud.mr_member.get_by_member_id(db=db, member_id=new_gr_mem.member_id)
            gr_mem_list.append(gr_user.member_id)
            # notify(receiver_uuid=gr_user_uuid.user_uuid, ...)
        group_list.append(gr_mem_list)

    return {'message': 'success', 'data':group_list}
