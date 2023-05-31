import json
from typing import Any

import requests
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.notifier import notify
from app.routers import deps

router = APIRouter()


@router.post("/", response_model=schemas.GroupAfterMatchingEvent)
async def initiate_matching_event(
    *,
    db: Session = Depends(deps.get_db),
    matching_room_in: schemas.MatchingRoomForEvent,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Initiate matching event.
    """
    matching_room = crud.matching_room.get_by_room_id(
        db=db, room_id=matching_room_in.room_id
    )
    if not matching_room:
        raise HTTPException(
            status_code=400,
            detail="Matching room with this room_id does not exist in this system.",
        )

    if matching_room.is_closed:
        raise HTTPException(
            status_code=400,
            detail="Matching room is already closed.",
        )

    """
    Call matching event micro-service
    """
    # return matching_event(db=db, matching_room=matching_room)
    logger.info("Start Micro service")
    url = "http://matching:8001/matching/create"
    payload = json.dumps(
        {
            "room_id": matching_room.room_id,
            "group_choice": matching_room_in.group_choice,
            "slot_choice": matching_room_in.slot_choice,
            "proximity": matching_room_in.proximity,
            "params": {
                "num_groups": matching_room_in.num_groups,
                "max_users": matching_room_in.max_users,
                "min_users": matching_room_in.min_users,
            },
        }
    )
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload)

    logger.info(response.text)

    if response.status_code == 200:
        # Close matching room
        matching_room = crud.matching_room.close_by_room_id(
            db=db, room_id=matching_room.room_id
        )

        """
        Create Group and GR_Member
        """
        result = json.loads(response.text)["groups"]
        # Get notify template_uuid
        notification_template = crud.notification_template.get_by_template_id(
            db=db, template_id="matching_result"
        )

        group_list = []
        group_id = 0
        for group in result:
            # Create Group
            group_id += 1
            new_group_schema = schemas.GroupCreate(
                name=matching_room.name + "_" + str(group_id),
                group_id=matching_room.room_id + "_" + str(group_id),
                room_uuid=matching_room.room_uuid,
            )
            new_group = crud.group.create(db=db, obj_in=new_group_schema)

            gr_mem_list = []
            for gr_member in result[group]:
                # Create GR_member
                new_gr_mem_schema = schemas.GR_MemberCreate(
                    member_id=gr_member,
                    group_uuid=new_group.group_uuid,
                    join_time=new_group.create_time,
                )
                new_gr_mem = crud.gr_member.create(db=db, obj_in=new_gr_mem_schema)

                """
                Call notification method for every Group Member
                """
                gr_user = crud.mr_member.get_by_member_id(
                    db=db, member_id=new_gr_mem.member_id
                )
                gr_mem_list.append(gr_user.member_id)

                # Create notify send object
                notification_send_object = (
                    schemas.NotificationSendObjectModelWithGroupID(
                        receiver_uuid=gr_user.user_uuid,
                        template_uuid=notification_template.template_uuid,
                        f_string=matching_room.name,
                        group_id=new_group.group_id,
                    )
                )
                await notify(db, notification_send_object)
            group_list.append(gr_mem_list)

        return {"message": "success", "data": group_list}

    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=json.loads(response.text)["detail"],
        )
