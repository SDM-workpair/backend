from typing import List


class Feature:
    def __init__(self, candidate_member_id_list: List[str]) -> None:
        self.candidate_member_id_list = candidate_member_id_list


class RandomFeature(Feature):
    def __init__(self, candidate_member_id_list: List[str]) -> None:
        super().__init__(candidate_member_id_list)


class HotPersonFeature(Feature):
    def __init__(
        self, candidate_member_id_list: List[str], popular_score_list: List[int]
    ) -> None:
        super().__init__(candidate_member_id_list)
        self.popular_score_list = popular_score_list
