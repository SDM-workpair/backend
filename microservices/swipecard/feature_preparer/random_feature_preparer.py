# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))
from sqlalchemy.orm import Session

from microservices.swipecard.core.recommend_feature import RandomFeature
from microservices.swipecard.feature_preparer.base_preparer import BasePreparer


class RandomFeaturePreparer(BasePreparer):
    def prepare(self, member_id: str, room_uuid: str, db: Session) -> RandomFeature:
        candidate_member_id_list = self.get_candidate_member_id(
            member_id, room_uuid, db
        )
        random_feature = RandomFeature(candidate_member_id_list)
        return random_feature
