# from app.schemas import SwipeCardRecommend
from typing import List

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))
from sqlalchemy.orm import Session

from microservices.swipecard.recommendation_strategy import RecommendationStrategy


class RecommendationContext:
    """
    推薦演算法 context class
    """

    strategy: RecommendationStrategy

    def __init__(self, strategy: RecommendationStrategy = None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def recommend(self, member_id, room_uuid, db: Session) -> List[str]:
        # 調用當前策略的推薦演算法，回傳5個要推薦的member_id 的 list
        return self.strategy.recommend(member_id, room_uuid, db)
