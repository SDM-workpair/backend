from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import ARRAY
from app import crud, schemas
from app.routers import deps
import loguru

router = APIRouter()

@router.post("/create-self-tag") #response-model
async def create_mr_member_tag(
    mr_member_tag_in: schemas.MR_Member_Tag_Create,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create MR_Member self-tag
    """
    # Check if MR_Member exists
    mr_member_in = crud.mr_member.get_by_member_id(
                                    db=db, 
                                    member_id=mr_member_tag_in.mr_member.member_id)
    if not mr_member_in:
        raise HTTPException(
            status_code=400,
            detail="Fail to find mr_member with this member_id.",
        )

    # Create MR_Member Self-Tag
    mr_member_tag_list = crud.mr_member_tag.create_tag(
                                            db=db,
                                            is_self_tag=True,
                                            is_find_tag=False,
                                            mr_member_tag_in= mr_member_tag_in)
    
    # 不知為啥回傳後只剩最後一個
    return {'message': 'success', 'data': mr_member_tag_list}


# TODO
@router.post("/create-find-tag") #response-model
async def create_mr_member_find_tag(
    mr_member_tag_in: schemas.MR_Member_Tag_Create,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create MR_Member find-tag
    """
     # Check if MR_Member exists
    mr_member_in = crud.mr_member.get_by_member_id(
                                    db=db, 
                                    member_id=mr_member_tag_in.mr_member.member_id)
    if not mr_member_in:
        raise HTTPException(
            status_code=400,
            detail="Fail to find mr_member with this member_id.",
        )

    # Create MR_Member Self-Tag
    mr_member_tag_list = crud.mr_member_tag.create_tag(
                                            db=db,
                                            is_self_tag=False,
                                            is_find_tag=True,
                                            mr_member_tag_in= mr_member_tag_in)
    
    return {'message': 'success', 'data':mr_member_tag_list}

