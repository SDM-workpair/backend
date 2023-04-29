from fastapi import Depends, FastAPI
from loguru import logger
from sqlalchemy.orm import Session

from . import crud
from .core.matching_event import OneTimeMatchingEventBuilder
from .database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/")
async def root(*, db: Session = Depends(get_db)):
    from app import crud

    user = crud.user.get_by_email(
        db, email="xghbpdyhrkeoxrqgxkjlgwxdydjcnpxx@example.com"
    )
    logger.info(user)
    return {"message": "Hello World"}


@app.post("/matching/create")
async def create_matching_event():
    """Create matching event"""

    logger.info("invoke mathcing event create")

    # Create the matching event
    small_data = [
        (1, [0, 1, 1, -1, 1]),
        (2, [-1, 0, 1, -1, 1]),
        (3, [1, -1, -1, 1, 1]),
        (4, [-1, 1, 0, 1, 1]),
        (5, [1, -1, -1, 1, 1]),
    ]

    config = {
        "group_choice": "random",
        "slot_choice": "fixed_group_amount",
        "params": {"num_groups": 3},
        "users_pref": small_data,
    }
    matching_event_builder = OneTimeMatchingEventBuilder()

    # Group the users using the chosen strategy
    groups = (
        matching_event_builder.set_total_users(len(config["users_pref"]))
        .set_strategy(config["group_choice"], config["slot_choice"])
        .set_slot_params(config["params"])
        .match(config["users_pref"])
    )

    return {"message": groups}


@app.get("/matching/{matching_id}")
async def get_by_matching_id(matching_id: int):
    """
    Get matching event by matching id
    """
    return {"message": "Hello World"}


@app.get("/matching/all/")
async def get_all_matching_event():
    """Get all matching event"""
    return {"message": "Hello World"}
