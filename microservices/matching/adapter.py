from typing import List, Tuple

from loguru import logger


class MatchingEventAdapter:
    def __init__(self) -> None:
        self._total_users = 0
        self._member_id_list = []
        self._users_pref: List[Tuple[int, List[int]]] = []


class MatchingRoomLikedHatedAdapter(MatchingEventAdapter):
    def __init__(self) -> None:
        super().__init__()

    def get_total_users(self):
        return self._total_users

    def get_member_id_list(self):
        return sorted(list(set(self._member_id_list)))

    def get_users_pref(self):
        return self._users_pref

    def set_total_users(self, total_users):
        self._total_users = total_users

    def add_member_id(self, member_id):
        self._member_id_list.append(member_id)

    def transform_user_pref(self, mr_members_pref):
        sorted_member_id_list = self.get_member_id_list()

        # turn member_id_list to dict
        # user_list_dict = {user_id: index}
        user_list_dict = {}
        for index, user_id in enumerate(sorted_member_id_list):
            user_list_dict[user_id] = index

        # generate empty 2d array
        user_pref_list = [
            [0] * self.get_total_users() for _ in range(self.get_total_users())
        ]

        # insert pref into 2d array
        for member_pref in mr_members_pref:
            user_id = member_pref.member_id
            target_member_id = member_pref.target_member_id

            # if member not in member list, skip
            if (
                user_id not in sorted_member_id_list
                or target_member_id not in sorted_member_id_list
            ):
                continue

            user_index = user_list_dict[user_id]
            target_index = user_list_dict[target_member_id]

            if member_pref.is_liked:
                user_pref_list[user_index][target_index] = 1
            elif member_pref.is_hated:
                user_pref_list[user_index][target_index] = -1

        logger.info(f"user_pref_list: {user_pref_list}")
        user_pref = []
        # turn 2d array to list of tuple
        for user_id in sorted_member_id_list:
            user_index = user_list_dict[user_id]
            user_pref.append(tuple((user_id, user_pref_list[user_index])))

        logger.info(f"user_pref: {user_pref}")
        self._users_pref = user_pref
