from typing import Any, List

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic.networks import EmailStr

from app import crud, models, schemas
from app.routers import deps
from app.core.config import settings

router = APIRouter()


@router.post("/my-list", response_model={})  # List[schemas.MatchingRoom])
def read_my_groups(
    db: Session = Depends(deps.get_db),
    user_email: str = ""  # ,
    # current_user: models.user = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve user's matching rooms.
    """
    groups = crud.group.search_with_user_and_name(
        db=db, user_email=user_email)
    return {'message': 'success', 'data': groups}


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
