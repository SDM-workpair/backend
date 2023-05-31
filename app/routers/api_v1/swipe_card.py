from typing import Any

import loguru
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.microservices.swipe_card.recommendation_context import RecommendationContext
from app.microservices.swipe_card.recommendation_strategy import RandomRecommendation
from app.routers import deps

router = APIRouter()
# create RecommendationContext instance
recommendation_context = RecommendationContext()
# Create recommend strategy instance
random_recommendation_strategy = RandomRecommendation()


@router.post("/swipe", response_model=schemas.SwipeCardPreferenceMessage)
def save_preference(
    *,
    db: Session = Depends(deps.get_db),
    swiped_card_in: schemas.SwipeCardPreference,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Save member's preference from the card he swiped.
    """
    try:
        swipe_card_preference = crud.swipe_card.save_preference(
            db, obj_in=swiped_card_in
        )
        return {"message": "success", "data": swipe_card_preference}
    except Exception as e:
        loguru.logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{e}",
        )


@router.post(
    "/swipe-recommend",
    response_model=schemas.swipe_card.SwipeCardMessage
    # "/swipe-recommend"
)
def get_recommendation(
    *,
    db: Session = Depends(deps.get_db),
    recommend_in: schemas.SwipeCardAskRecommend,  # member_id(或者不傳member_id,用current_user去撈MR_member的member_id?), room_uuid
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    return a swipe card recommenation list
    """
    recommendation_context.set_strategy(random_recommendation_strategy)
    recommended_member_id_list = recommendation_context.recommend(
        recommend_in.member_id, recommend_in.room_id, db
    )

    # generate recommen card for each to-be-recommended member
    recommend_card_list = []
    for rcmd_member_id in recommended_member_id_list:
        # get find tag, self tag by member_id and room_uuid
        self_tag = jsonable_encoder(
            crud.swipe_card.get_self_tag_by_member_id_and_room_id(
                db=db, member_id=str(rcmd_member_id), room_id=recommend_in.room_id
            )
        )
        self_tag_text = [t["tag_text"] for t in self_tag]
        find_tag = jsonable_encoder(
            crud.swipe_card.get_find_tag_by_member_id_and_room_id(
                db=db, member_id=str(rcmd_member_id), room_id=recommend_in.room_id
            )
        )
        find_tag_text = [t["tag_text"] for t in find_tag]

        # get member profile (image, name)
        user = crud.swipe_card.get_user_profile_by_member_id(
            db=db, member_id=rcmd_member_id
        )
        image = user.image
        name = user.name

        # make a recommendation list
        swipe_card = {
            "member_id": recommend_in.member_id,
            "room_id": recommend_in.room_id,
            "recommended_member_id": rcmd_member_id,
            "self_tag_text": self_tag_text,
            "find_tag_text": find_tag_text,
            "image": image,
            "name": name,
        }
        recommend_card_list.append(swipe_card)

    return {"message": "success", "data": recommend_card_list}
    # return {"recommend_card_list": recommended_member_id_list, "self_tag": self_tag_text, "finf_tag": find_tag_text}
