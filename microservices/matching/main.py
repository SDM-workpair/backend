import sys
import traceback

from fastapi import Depends, FastAPI, HTTPException, Response, status
from loguru import logger
from sqlalchemy.orm import Session

from microservices.matching.adapter import MatchingRoomLikedHatedAdapter
from microservices.matching.core.matching_event import OneTimeMatchingEventBuilder
from microservices.matching.crud import CRUDLikedHatedMember
from microservices.matching.database import SessionLocal
from microservices.matching.schema import MatchingEvent, MatchingGroups, Message

app = FastAPI()

base_response = {
    500: {"model": Message},
    404: {"model": Message},
    501: {"model": Message},
}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/matching/create/test", responses={**base_response, 200: {"model": MatchingGroups}}
)
async def create_matching_event_test(config: MatchingEvent):
    """Create test matching event"""

    logger.info("invoke mathcing event create")

    # Create the matching event
    small_data = [
        (1, [0, 1, 1, -1, 1]),
        (2, [-1, 0, 1, -1, 1]),
        (3, [1, -1, -1, 1, 1]),
        (4, [-1, 1, 0, 1, 1]),
        (5, [1, -1, -1, 1, 1]),
    ]

    config = {
        "group_choice": "random",
        "slot_choice": "fixed_group",
        "params": {"num_groups": 3},
        "users_pref": small_data,
    }
    matching_event_builder = OneTimeMatchingEventBuilder()

    # Group the users using the chosen strategy
    groups = (
        matching_event_builder.set_total_users(len(config["users_pref"]))
        .set_strategy(config["group_choice"], config["slot_choice"])
        .set_slot_params(config["params"])
        .match(config["users_pref"])
    )

    return {"groups": groups}


@app.post(
    "/matching/create", responses={**base_response, 200: {"model": MatchingGroups}}
)
async def create_matching_event(
    config: MatchingEvent, *, db: Session = Depends(get_db), response: Response
):
    """Create matching event"""

    logger.info(f"config: {config}")
    adapter = MatchingRoomLikedHatedAdapter()

    logger.info("invoke mathcing event create")
    try:
        matching_room = await CRUDLikedHatedMember.get_matching_room(
            db=db, room_id=config.room_id
        )
    except Exception as e:
        logger.error(getexception(e))
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": "get_matching_room query error"}

    if not matching_room:
        raise HTTPException(
            status_code=404,
            detail="Matching room does not exist",
        )

    try:
        logger.info("get_member_in_matching_room")
        mr_members = await CRUDLikedHatedMember.get_member_in_matching_room(
            db=db, room_uuid=matching_room.room_uuid
        )
        adapter.set_total_users(len(mr_members))
        for mr_member in mr_members:
            adapter.add_member_id(mr_member.member_id)
    except Exception as e:
        logger.error(getexception(e))
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": "get_matching_room_members query error"}

    if adapter.get_total_users() < 1:
        raise HTTPException(
            status_code=404,
            detail="Matching room is empty",
        )

    try:
        logger.info("get_mr_user_pref_in_matching_room")
        mr_members_pref = await CRUDLikedHatedMember.get_mr_user_pref_in_matching_room(
            db=db, room_uuid=matching_room.room_uuid
        )
    except Exception as e:
        logger.error(getexception(e))
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": "get_mr_user_pref_in_matching_room query error"}

    try:
        await adapter.transform_user_pref(mr_members_pref)
    except Exception as e:
        logger.error(getexception(e))
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": "transform_user_pref query error"}

    try:
        logger.info("start building matching event")
        # start building matching event
        config = {
            "group_choice": config.group_choice,
            "slot_choice": config.slot_choice,
            "params": config.params,
            "users_pref": adapter.get_users_pref(),
        }
        matching_event_builder = OneTimeMatchingEventBuilder()

        # Group the users using the chosen strategy
        groups = (
            matching_event_builder.set_total_users(len(config["users_pref"]))
            .set_strategy(config["group_choice"], config["slot_choice"])
            .set_slot_params(config["params"])
            .match(config["users_pref"])
        )
    except Exception as e:
        logger.error(getexception(e))
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"detail": f"matching event builder error, {e}"}

    return {"groups": groups}


@app.get("/matching/{matching_id}")
async def get_by_matching_id(matching_id: int, response: Response):
    """
    Get matching event by matching id
    """
    response.status_code = status.HTTP_501_NOT_IMPLEMENTED
    return {"detail": "Hello World"}


@app.get("/matching/all/")
async def get_all_matching_event(response: Response):
    """Get all matching event"""
    response.status_code = status.HTTP_501_NOT_IMPLEMENTED
    return {"detail": "Hello World"}


@app.get("/healthchecker")
async def healthchecker():
    return {"msg": "Hello World"}


def getexception(e):
    error_class = e.__class__.__name__  # 取得錯誤類型
    detail = e.args[0]  # 取得詳細內容
    cl, exc, tb = sys.exc_info()  # 取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
    fileName = lastCallStack[0]  # 取得發生的檔案名稱
    lineNum = lastCallStack[1]  # 取得發生的行號
    funcName = lastCallStack[2]  # 取得發生的函數名稱

    errMsg = 'File "{}", line {}, in {}: [{}] {}'.format(
        fileName, lineNum, funcName, error_class, detail
    )
    print(errMsg)
