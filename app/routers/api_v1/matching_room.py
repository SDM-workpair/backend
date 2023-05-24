from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.routers import deps

router = APIRouter()


@router.get("/my-list", response_model=schemas.MatchingRoomsWithMessage)
def read_my_matching_rooms(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve user's matching rooms with their member_id in each matching room.
    """
    matching_rooms = crud.matching_room.search_with_user_and_name(
        db=db, user_uuid=current_user.user_uuid, is_query_with_user=True
    )
    return {"message": "success", "data": matching_rooms}


@router.post("/create", response_model=schemas.MatchingRoomWithMessage)
def create_matching_room(
    *,
    db: Session = Depends(deps.get_db),
    matching_room_in: schemas.MatchingRoomReq,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new matching room.
    """
    matching_room = crud.matching_room.create(db, obj_in=matching_room_in)

    return {"message": "success", "data": matching_room}


@router.post("/rcmed-tag", response_model=schemas.Tag_Res)
def get_rcmed_tag(
    *,
    db: Session = Depends(deps.get_db),
    matching_room_in: schemas.MatchingRoomBase,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get recommended tag for matching room.
    """
    # Check if matching room exists.
    matching_room = crud.matching_room.get_by_room_id(
        db=db, room_id=matching_room_in.room_id
    )
    if not matching_room:
        raise HTTPException(
            status_code=400,
            detail="Matching room does not exist in the system.",
        )

    # Get top five tags
    tags = crud.tag.get_rcmed_tags_by_room_uuid(
        db=db, room_uuid=matching_room.room_uuid, tag_num=5
    )
    return {"message": "success", "data": tags}


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
