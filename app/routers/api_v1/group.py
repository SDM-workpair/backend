from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.routers import deps

router = APIRouter()


@router.get("/my-list", response_model=schemas.GroupWithMessage)
def read_my_groups(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve user's groups.
    """
    groups = crud.group.search_with_user_and_name(
        db=db, user_uuid=current_user.user_uuid
    )
    return {"message": "success", "data": groups}


@router.post("/members", response_model=schemas.UsersMessage)
def get_group_members(
    gr_member_search_in: schemas.GR_MemberWithSearch,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve group members with group_id.
    """
    if gr_member_search_in.group_id == "":
        raise HTTPException(
            status_code=400,
            detail="Fail to get group members. Missing parameter: group_id.",
        )
    members = crud.gr_member.get_all_members_by_group_id(
        db=db, group_id=gr_member_search_in.group_id
    )
    return {"message": "success", "data": members}


# # TODO: unfinished
# @router.post("/", response_model=schemas.MatchingRoom)
# def create_group(
#     *,
#     db: Session = Depends(deps.get_db),
#     group_in: schemas.MatchingRoomCreate,
#     current_user: models.user = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Create new matching room.
#     """
#     group = crud.group.get_by_group_id(
#         db, group_id=group_in.group_id)
#     if group:
#         raise HTTPException(
#             status_code=400,
#             detail="The group with this group_id already exists in the system.",
#         )
#     group = crud.group.create(db, obj_in=get_by_group_id)
#     return group  # TODO: need to revise response_model


# # TODO: unfinished
# @router.delete("/", response_model=dict)
# def delete_group(
#     db: Session = Depends(deps.get_db),
#     group_id: str = "",
#     current_user: models.user = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete group with group_id.
#     """
#     group = crud.group.get_by_group_id(
#         db, group_id=group_id)
#     if not group:
#         raise HTTPException(
#             status_code=400,
#             detail="No group to delete.",
#         )
#     isDeleteSuccessfully = crud.group.delete(db, group)
#     if isDeleteSuccessfully:
#         return {"message": "Success"}
#     else:
#         return {"message": "Fail"}
