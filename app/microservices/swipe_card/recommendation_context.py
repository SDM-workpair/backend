from typing import List

from sqlalchemy.orm import Session

# from app.schemas import SwipeCardRecommend
from .recommendation_strategy import RecommendationStrategy


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
