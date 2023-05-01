from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.routers import deps

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
    # matching_event(matching_room)

    return {'message': 'success', 'data':'group data'}
