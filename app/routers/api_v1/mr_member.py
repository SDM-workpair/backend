from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.routers import deps

router = APIRouter()


@router.post("/create", response_model=schemas.MR_Member_Create_Res)
async def join_matching_room(
    mr_member_in: schemas.MR_Member_Req,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create MR_Member
    """
    # Check if user exists
    user = await crud.user.get_by_email(db=db, email=mr_member_in.user.email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User does not exist in the system.",
        )

    # Check if matching room exists
    matching_room = await crud.matching_room.get_by_room_id(
        db=db, room_id=mr_member_in.matching_room.room_id
    )
    if not matching_room:
        raise HTTPException(
            status_code=400,
            detail="Matching room does not exist in the system.",
        )

    # Check if user already in matching room
    mr_member = await crud.mr_member.get_by_room_uuid_and_user_uuid(
        db=db, room_uuid=matching_room.room_uuid, user_uuid=user.user_uuid
    )
    if mr_member:
        raise HTTPException(
            status_code=400,
            detail="User already in the matching room.",
        )

    # Create MR_Member
    new_mr_member = await crud.mr_member.create(
        db=db, user_uuid=user.user_uuid, room_uuid=matching_room.room_uuid
    )

    # Recreate response model
    data = {
        "member_id": new_mr_member.member_id,
        "user": {"email": user.email, "is_admin": user.is_admin, "name": user.name},
        "matching_room": {"room_id": matching_room.room_id},
    }

    return {"message": "success", "data": data}


@router.delete("/", response_model=schemas.MR_Member_Del_Res)
async def leave_matching_room(
    mr_member_in: schemas.MR_Member_Req,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Leave matching room and delete MR_Member
    """
    # Check if user exists
    user = await crud.user.get_by_email(db=db, email=mr_member_in.user.email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User does not exist in the system.",
        )

    # Check if matching room exists
    matching_room = await crud.matching_room.get_by_room_id(
        db=db, room_id=mr_member_in.matching_room.room_id
    )
    if not matching_room:
        raise HTTPException(
            status_code=400,
            detail="Matching room does not exist in the system.",
        )

    # Check if user is in matching room
    mr_member = await crud.mr_member.get_by_room_uuid_and_user_uuid(
        db=db, room_uuid=matching_room.room_uuid, user_uuid=user.user_uuid
    )
    if not mr_member:
        raise HTTPException(
            status_code=400,
            detail="User is not in the matching room.",
        )

    # Delete MR_Member
    result = await crud.mr_member.delete(db=db, db_obj=mr_member)

    if result:
        return {"message": "success"}

    return Response(status_code=status.HTTP_204_NO_CONTENT)
