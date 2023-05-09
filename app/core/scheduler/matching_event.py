from sqlalchemy import event
import loguru
from app.models.matching_room import MatchingRoom
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from tzlocal import get_localzone
from app import crud, models, schemas
from app.notifier import notify
from app.routers import deps
import json
import requests
from sqlalchemy.orm import Session
from fastapi import Depends


"""
Matching event scheduler
"""
scheduler = BackgroundScheduler()
scheduler.start()

async def matching_event(matching_room: MatchingRoom, db: Session = Depends(deps.get_db)):
    loguru.logger.info("run matching_event function")
    """
    Call matching event micro-service
    """
    url = "http://matching:8001/matching/create"
    payload = json.dumps(
        {
            "room_id": matching_room.room_id,
            "group_choice": "random",
            "slot_choice": "fixed_min",
            "params": {
                # "num_groups": 3,
                # "max_users": 6,
                "min_users": matching_room.min_member_num
            },
        }
    )
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload)
    loguru.logger.info(response.text)
    result = json.loads(response.text)["groups"]
    """
    Create Group and GR_Member
    """
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
            notification_send_object = schemas.NotificationSendObjectModel(
                receiver_uuid=gr_user.user_uuid,
                template_uuid=notification_template.template_uuid,
                f_string=matching_room.name,
            )
            await notify(db, notification_send_object)
        group_list.append(gr_mem_list)
    return

def schedule_matching_event(matching_room: MatchingRoom):
    loguru.logger.info(matching_room)
    # call matching_event function
    due_time = matching_room.due_time
    scheduler.add_job(
        matching_event,
        'date',
        run_date=due_time,
        args=[matching_room]
    )
    return


@event.listens_for(MatchingRoom, 'after_insert')
def schedule_matching_room(mapper, connection, matching_room):
    "listen for the 'after_insert' event"
    schedule_matching_event(matching_room=matching_room)
    

@atexit.register
def shutdown_scheduler():
    scheduler.shutdown()
