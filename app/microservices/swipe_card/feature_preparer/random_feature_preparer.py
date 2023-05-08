from sqlalchemy.orm import Session

from ..recommend_feature import RandomFeature
from .base_preparer import BasePreparer


class RandomFeaturePreparer(BasePreparer):
    def prepare(self, member_id: str, room_uuid: str, db: Session) -> RandomFeature:
        candidate_member_id_list = self.get_candidate_member_id(
            member_id, room_uuid, db
        )
        random_feature = RandomFeature(candidate_member_id_list)
        return random_feature
