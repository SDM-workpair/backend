from typing import Any

from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from microservices.swipecard import crud
from microservices.swipecard.database import SessionLocal
from microservices.swipecard.recommendation_context import RecommendationContext
from microservices.swipecard.recommendation_strategy import RandomRecommendation
from microservices.swipecard.schemas import (
    SwipeCardAskRecommend,
    SwipeCardMessage,
    SwipeCardPreference,
    SwipeCardPreferenceMessage,
)

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))


app = FastAPI()

# create RecommendationContext instance
recommendation_context = RecommendationContext()
# Create recommend strategy instance
random_recommendation_strategy = RandomRecommendation()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/swipe-card/swipe", response_model=SwipeCardPreferenceMessage)
async def save_preference(
    *,
    db: Session = Depends(get_db),
    swiped_card_in: SwipeCardPreference,
) -> Any:
    """
    Save member's preference from the card he swiped.
    """
    swipe_card_preference = crud.swipe_card.save_preference(db, obj_in=swiped_card_in)
    return {"message": "success", "data": swipe_card_preference}


@app.post("/swipe-card/swipe-recommend", response_model=SwipeCardMessage)
async def get_recommendation(
    *,
    db: Session = Depends(get_db),
    recommend_in: SwipeCardAskRecommend,  # member_id(或者不傳member_id,用current_user去撈MR_member的member_id?), room_uuid
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


@app.get("/healthchecker")
def healthchecker():
    return {"msg": "Hi it's swipecard microservice :)"}
