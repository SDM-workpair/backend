from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.routers import deps
import loguru

router = APIRouter()


@router.post("/create")
def join_matching_room(
    mr_member_in: schemas.MR_Member_Req,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create MR_Member
    """
    # Check if user exists
    user = crud.user.get_by_email(db=db, email=mr_member_in.user.email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User does not exist in the system.",
        )

    # Check if matching room exists
    matching_room = crud.matching_room.get_by_room_id(db=db, room_id=mr_member_in.matching_room.room_id)
    if not matching_room:
        raise HTTPException(
            status_code=400,
            detail="Matching room does not exist in the system.",
        )

    # Check if user already in matching room
    mr_member = crud.mr_member.get_by_room_uuid_and_user_uuid(
                                    db=db, 
                                    room_uuid=matching_room.room_uuid, 
                                    user_uuid=user.user_uuid
                                )
    if mr_member:
        raise HTTPException(
            status_code=400,
            detail="User already in the matching room.",
        )

    # Create MR_Member
    new_mr_member = crud.mr_member.create(
                                    db=db,
                                    user_uuid=user.user_uuid,
                                    room_uuid=matching_room.room_uuid
                                )

    return {'message': 'success', 'data': new_mr_member}