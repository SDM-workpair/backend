import json
from typing import Any

import requests
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.notifier import notify
from app.routers import deps

# from app.core.scheduler import matching_event

router = APIRouter()



@router.post("/matching")
def get_matching_event_health_checker(
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    url = "http://matching:8001/healthchecker"
    response = requests.request("POST", url)
    return json.loads(response.text)

@router.post("/swipe-card")
def get_matching_event_health_checker(
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    url = ""
    response = requests.request("POST", url)
    return json.loads(response.text)