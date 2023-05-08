from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.routers import deps

router = APIRouter()


@router.post("/matching-room/list", response_model=schemas.MatchingRoomsWithMessage)
def search_matching_rooms(
    mr_search_in: schemas.MatchingRoomWithSearch,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve matching rooms.
    """
    if mr_search_in.query_all:
        matching_rooms = crud.matching_room.search_with_user_and_name(
            db=db, name=mr_search_in.prompt
        )
    else:  # query with user authentication
        matching_rooms = crud.matching_room.search_with_user_and_name(
            db=db,
            user_uuid=current_user.user_uuid,
            name=mr_search_in.prompt,
        )
    return {"message": "success", "data": matching_rooms}


@router.post("/group/list", response_model=schemas.GroupWithMessage)
def search_my_groups(
    group_search_in: schemas.GroupWithSearch,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve groups.
    """
    groups = crud.group.search_with_user_and_name(
        db=db,
        user_uuid=current_user.user_uuid,
        name=group_search_in.prompt,
    )
    return {"message": "success", "data": groups}


@router.post("/matching-room/test", response_model=schemas.MatchingRoomsWithMessage)
def search_matching_rooms_test(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve matching rooms test.
    """
    matching_rooms = crud.matching_room.search_with_user_and_name(db=db, name="")
    return {"message": "success", "data": matching_rooms}
