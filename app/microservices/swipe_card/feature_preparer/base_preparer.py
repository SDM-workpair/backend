from abc import ABC, abstractmethod
from typing import Any, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud


class BasePreparer(ABC):
    @abstractmethod
    def prepare(self, member_id: str, room_id: str, db: Session) -> Any:
        pass

    def get_candidate_member_id(
        self, member_id: str, room_id: str, db: Session
    ) -> List[str]:
        # 1. get all members by room_id
        mr_member = jsonable_encoder(
            crud.swipe_card.get_mr_member_by_room_id(db=db, room_id=room_id)
        )

        # 2. check if there is any members in matching room
        if mr_member:
            all_mr_member_id_list = [m["member_id"] for m in mr_member]

            # 3. if yes, query MR_Liked_Hated_Member table by member_id
            mr_liked_hated_member = jsonable_encoder(
                crud.swipe_card.get_preference_by_member_id_and_room_id(
                    db=db, member_id=member_id, room_id=room_id
                )
            )
            rcmd_member_id = [
                rcmd_member["target_member_id"] for rcmd_member in mr_liked_hated_member
            ]

            # 4. compare it with all the members in matching room to get those who are not recommended
            unrcmd_member_id = (
                set(all_mr_member_id_list) - set(rcmd_member_id) - set([int(member_id)])
            )
            if unrcmd_member_id:
                candidate_member_id_list = list(unrcmd_member_id)
            else:
                candidate_member_id_list = []

        else:
            candidate_member_id_list = []

        return candidate_member_id_list
