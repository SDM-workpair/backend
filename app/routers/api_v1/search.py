from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.routers import deps

router = APIRouter()


@router.post("/matching-room/list", response_model=schemas.MatchingRoomsWithMessage)
def search_matching_rooms(
    mr_search_in: schemas.MatchingRoomWithSearch,
    db: Session = Depends(deps.get_db),
    # current_user: models.user = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve matching rooms.
    """
    if mr_search_in.query_all:
        matching_rooms = crud.matching_room.search_with_user_and_name(
            db=db, name=mr_search_in.prompt
        )
    else:  # query with user authentication
        #  先看user_email是否找得到user再去query matching room
        if mr_search_in.user_email == "" or mr_search_in.user_email is None:
            raise HTTPException(
                status_code=400,
                detail="Fail to retrieve user's matching room. Missing parameter: email.",
            )
        user = crud.user.get_by_email(db=db, email=mr_search_in.user_email)
        if not user:
            raise HTTPException(
                status_code=400,
                detail="Fail to find user with this email.",
            )
        matching_rooms = crud.matching_room.search_with_user_and_name(
            db=db, user_uuid=user.user_uuid, name=mr_search_in.prompt
        )
    return {"message": "success", "data": matching_rooms}


@router.post("/group/list", response_model=schemas.GroupWithMessage)
def search_my_groups(
    group_search_in: schemas.GroupWithSearch,
    db: Session = Depends(deps.get_db),
    # current_user: models.user = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve groups.
    """
    #  先看user_email是否找得到user再去query group
    if group_search_in.user_email == "" or group_search_in.user_email is None:
        raise HTTPException(
            status_code=400,
            detail="Fail to retrieve user's group. Missing parameter: email.",
        )
    user = crud.user.get_by_email(db=db, email=group_search_in.user_email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Fail to find user with this email.",
        )
    groups = crud.group.search_with_user_and_name(
        db=db, user_uuid=user.user_uuid, name=group_search_in.prompt
    )
    return {"message": "success", "data": groups}
