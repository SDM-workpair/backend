from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.routers import deps

router = APIRouter()


@router.post("/my-list", response_model=schemas.MatchingRoomsWithMessage)
def read_my_matching_rooms(
    user_in: schemas.User,
    db: Session = Depends(deps.get_db),
    # current_user: models.user = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve user's matching rooms.
    """
    #  先看email是否找得到user再去query matching room
    if user_in.email == "" or user_in.email is None:
        raise HTTPException(
            status_code=400,
            detail="Fail to retrieve user's matching room. Missing parameter: email.",
        )
    user = crud.user.get_by_email(db=db, email=user_in.email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Fail to find user with this email.",
        )
    matching_rooms = crud.matching_room.search_with_user_and_name(
        db=db, user_uuid=user.user_uuid
    )
    return {"message": "success", "data": matching_rooms}


@router.post("/create", response_model=schemas.MatchingRoomWithMessage)
def create_matching_room(
    *,
    db: Session = Depends(deps.get_db),
    matching_room_in: schemas.MatchingRoomCreate,
    # current_user: models.user = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new matching room.
    """
    # room_id -> 我們給的 四碼or六碼
    matching_room = crud.matching_room.get_by_room_id(
        db, room_id=matching_room_in.room_id)
    if matching_room:
        # 改意思
        raise HTTPException(
            status_code=400,
            detail="The matching room with this room_id already exists in the system.",
        )
    matching_room = crud.matching_room.create(db, obj_in=matching_room_in)
    return {'message': 'success', 'data': matching_room}





# @router.delete("/", response_model=schemas.MatchingRoomWithMessage)
# def delete_matching_room(
#     db: Session = Depends(deps.get_db),
#     room_id: str = "",
#     current_user: models.user = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete matching room with room_id.
#     """
#     if (room_id == '' or room_id is None):
#         raise HTTPException(
#             status_code=400,
#             detail="Fail to delete matching room. Missing parameter: room_id"
#         )
#     matching_room = crud.matching_room.get_by_room_id(
#         db, room_id=room_id)
#     if not matching_room:
#         raise HTTPException(
#             status_code=400,
#             detail="No matching room to delete.",
#         )
#     isDeleteSuccessfully = crud.matching_room.delete(db, room_id)
#     if isDeleteSuccessfully:
#         return {'message': 'success', 'data': None}
#     else:
#         return {'message': 'fail', 'data': None}
