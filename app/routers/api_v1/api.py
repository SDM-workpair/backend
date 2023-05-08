from fastapi import APIRouter

from app.routers.api_v1 import (
    auth,
    group,
    health_checker,
    login,
    matching_event,
    matching_room,
    mr_member,
    mr_member_tag,
    notification,
    search,
    swipe_card,
    user,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.mount("/google-auth", auth.auth_app)
api_router.include_router(
    matching_room.router, prefix="/matching-room", tags=["matching-room"]
)
api_router.include_router(group.router, prefix="/group", tags=["group"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(
    notification.router, prefix="/notification", tags=["notification"]
)
api_router.include_router(
    matching_event.router, prefix="/matching-event", tags=["matching-event"]
)
api_router.include_router(swipe_card.router, prefix="/swipe-card", tags=["swipe-card"])
api_router.include_router(mr_member.router, prefix="/mr-member", tags=["mr-member"])
api_router.include_router(
    mr_member_tag.router, prefix="/mr-member-tag", tags=["mr-member-tag"]
)
api_router.include_router(
    health_checker.router, prefix="/health-checker", tags=["health-checker"]
)
