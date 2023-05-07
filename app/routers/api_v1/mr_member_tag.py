from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.routers import deps

router = APIRouter()


@router.post("/create-self-tag", response_model=schemas.MR_Member_Tag_Res)
async def create_mr_member_self_tag(
    mr_member_tag_in: schemas.MR_Member_Tag_Create,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create MR_Member self-tag
    """
    # Check if MR_Member exists
    mr_member_in = await crud.mr_member.get_by_member_id(
        db=db, member_id=mr_member_tag_in.mr_member.member_id
    )
    if not mr_member_in:
        raise HTTPException(
            status_code=400,
            detail="Fail to find mr_member with this member_id.",
        )

    # Create MR_Member Self-Tag
    mr_member_tag_list = await crud.mr_member_tag.create_tag(
        db=db, is_self_tag=True, is_find_tag=False, mr_member_tag_in=mr_member_tag_in
    )

    return {"message": "success", "data": mr_member_tag_list}


@router.post("/create-find-tag", response_model=schemas.MR_Member_Tag_Res)
async def create_mr_member_find_tag(
    mr_member_tag_in: schemas.MR_Member_Tag_Create,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create MR_Member find-tag
    """
    # Check if MR_Member exists
    mr_member_in = await crud.mr_member.get_by_member_id(
        db=db, member_id=mr_member_tag_in.mr_member.member_id
    )
    if not mr_member_in:
        raise HTTPException(
            status_code=400,
            detail="Fail to find mr_member with this member_id.",
        )

    # Create MR_Member Find-Tag
    mr_member_tag_list = await crud.mr_member_tag.create_tag(
        db=db, is_self_tag=False, is_find_tag=True, mr_member_tag_in=mr_member_tag_in
    )

    return {"message": "success", "data": mr_member_tag_list}
