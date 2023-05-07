from typing import Any

from fastapi import APIRouter, Depends
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
    Retrieve user's matching rooms.
    """
    matching_rooms = crud.matching_room.search_with_user_and_name(
        db=db, user_uuid=current_user.user_uuid
    )
    return {"message": "success", "data": matching_rooms}


@router.post("/create", response_model=schemas.MatchingRoomWithRoomId)
async def create_matching_room(
    *,
    db: Session = Depends(deps.get_db),
    matching_room_in: schemas.MatchingRoomReq,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new matching room.
    """
    matching_room = await crud.matching_room.create(db, obj_in=matching_room_in)

    return {"message": "success", "room_id": matching_room.room_id}


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
