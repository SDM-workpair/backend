import random
from abc import ABC, abstractmethod
from typing import List, Tuple

from loguru import logger
from numpy import array, dot, linalg, zeros


class GroupingStrategy(ABC):
    @abstractmethod
    def group_users(
        self, users: List[Tuple[int, List[int]]], num_groups: int
    ) -> List[List[int]]:
        pass


class TinderGrouping(GroupingStrategy):
    def group_users(
        self, users: List[Tuple[int, List[int]]], slots: List[int]
    ) -> List[List[List[int]]]:
        num_groups = len(slots)
        group_index = 0
        groups = {i: [] for i in range(num_groups)}
        users_left = users[:]
        popularity = users[:]

        users_prefs = array([x[1] for x in users])
        like_sum = users_prefs.sum(axis=0)

        # sort popularity by like_sum
        popularity = [x for _, x in sorted(zip(like_sum, popularity), reverse=True)]

        logger.info("popularity", [x[0] for x in popularity])

        while users_left:
            leader = None

            for user in popularity:
                if user in users_left:
                    leader = user
                    break
            logger.info(f"leader is {leader}")
            group_size = min(len(users_left), slots[group_index])
            group = [leader[0]]
            users_left.remove(leader)

            while len(group) < group_size and users_left:
                candidate = None

                # sort leader's preference
                leader_pref = leader[1]
                leader_pref_sorted = [
                    x for _, x in sorted(zip(like_sum, leader_pref), reverse=True)
                ]

                # find user that the leader like
                for target, pref in zip(popularity, leader_pref_sorted):
                    # if pref == 1, add to group
                    if pref == 1 and target in users_left and target not in group[1:]:
                        logger.info(f"leader {leader[0]} like {target[0]}")
                        candidate = target
                        break

                # if leader doesn't like anyone, pick the most popular user
                if candidate is None:
                    for user in popularity:
                        if user in users_left and user not in group[1:]:
                            candidate = user
                            break

                if candidate:
                    group.append(candidate[0])
                    users_left.remove(candidate)
            groups[group_index] += group

            group_index += 1
            if group_index >= num_groups:
                group_index = 0
        return groups


class RandomGrouping(GroupingStrategy):
    def group_users(
        self, users: List[Tuple[int, List[int]]], slots: List[int]
    ) -> List[List[List[int]]]:
        num_groups = len(slots)
        groups = {i: [] for i in range(num_groups)}
        users_left = users[:]
        slot_left = sum(slots)

        # Randomly assign users to groups
        while users_left and slot_left > 0:
            group_index = random.randint(0, num_groups - 1)
            # logger.info("groups", groups)
            # logger.info("group_index: ", group_index)
            if len(groups[group_index]) < slots[group_index]:
                user = users_left.pop(0)
                groups[group_index].append(user[0])
                slot_left -= 1
        return groups


class SimilarityGrouping(GroupingStrategy):
    def group_users(
        self, users: List[Tuple[int, List[int]]], slots: List[int]
    ) -> List[List[List[int]]]:
        num_users = len(users)
        num_groups = len(slots)

        # Compute pairwise cosine similarity matrix
        sim_matrix = zeros((num_users, num_users))
        for i in range(num_users):
            for j in range(i + 1, num_users):
                sim = dot(users[i][1], users[j][1]) / (
                    linalg.norm(users[i][1]) * linalg.norm(users[j][1])
                )
                sim_matrix[i][j] = sim
                sim_matrix[j][i] = sim

        # Group users based on cosine similarity
        groups = {i: [] for i in range(num_groups)}
        assigned_users = set()
        for i in range(num_groups):
            group_size = slots[i]
            group = []
            while len(group) < group_size and len(assigned_users) < num_users:
                remaining_users = set(range(num_users)) - assigned_users
                if remaining_users:
                    user_id = max(
                        remaining_users,
                        key=lambda u: sum(sim_matrix[u][v] for v in assigned_users),
                    )
                    group.append(user_id)
                    assigned_users.add(user_id)
            groups[i] = [users[user_id][0] for user_id in group]

        return groups


if __name__ == "__main__":
    users_pref = [
        (1, [0, 1, 1, -1, 1, 0, 1]),
        (2, [-1, 0, 1, -1, 1, 0, 1]),
        (3, [-1, 1, -1, 1, 1, 0, 1]),
        (4, [-1, 1, 0, -1, 1, 0, 1]),
        (5, [-1, 1, 0, -1, 1, 0, 0]),
        (7, [-1, 1, 0, 1, -1, 0, 0]),
        (6, [-1, 1, 0, 1, -1, 1, 0]),
    ]

    users_pref_one = [(1, [0, 1, 1, -1])]

    # algorithm testing
    logger.info("test")
    slots = [4, 3]

    logger.info("\nTinder")
    tg = TinderGrouping()
    groups_tinder = tg.group_users(users_pref, slots)
    for i, group in groups_tinder.items():
        logger.info(f"Group {i+1}: {group}")

    logger.info("\nTinder")
    rg = TinderGrouping()
    groups_random = rg.group_users(users_pref, slots)
    for i, group in groups_random.items():
        logger.info(f"Group {i+1}: {group}")

    logger.info("\nTinder edge 1 user")
    rg = TinderGrouping()
    groups_random = rg.group_users(users_pref_one, [1])
    for i, group in groups_random.items():
        logger.info(f"Group {i+1}: {group}")

    logger.info("\nTinder edge 2 groups")
    rg = TinderGrouping()
    groups_random = rg.group_users(users_pref, [1, 3])
    for i, group in groups_random.items():
        logger.info(f"Group {i+1}: {group}")

    logger.info("\nTinder edge 1 slot")
    rg = TinderGrouping()
    groups_random = rg.group_users(users_pref, slots=[3])
    for i, group in groups_random.items():
        logger.info(f"Group {i+1}: {group}")

    logger.info("\nTinder edge more slot")
    rg = TinderGrouping()
    groups_random = rg.group_users(users_pref, slots=[3, 3, 3, 3, 3])
    for i, group in groups_random.items():
        logger.info(f"Group {i+1}: {group}")

    logger.info("\nTinder")
    sg = TinderGrouping()
    groups = sg.group_users(users_pref, slots)
    for i, group in groups.items():
        logger.info(f"Group {i+1}: {group}")

    logger.info("\nTinder")
    sg = TinderGrouping()
    groups = sg.group_users(users_pref, slots=[3])
    for i, group in groups.items():
        logger.info(f"Group {i+1}: {group}")

    users_pref_like_second = [
        (1, [0, 1, 1, -1, 1, 0, 1]),
        (2, [-1, 0, 1, -1, 1, -1, 1]),
        (3, [-1, 1, -1, 1, 1, 0, 1]),
        (4, [-1, 1, -1, -1, 1, 0, 1]),
        (5, [-1, 1, 0, -1, 1, 1, 0]),
        (6, [-1, 1, 0, 1, -1, 1, 0]),
        (7, [-1, 1, 0, 1, -1, 1, 0]),
    ]

    logger.info("\nTinder")
    tg = TinderGrouping()
    groups_tinder = tg.group_users(users_pref_like_second, slots)
    for i, group in groups_tinder.items():
        logger.info(f"Group {i+1}: {group}")

    users_pref_like_third = [
        (3, [0, -1, 1, -1]),
        (4, [1, 0, 1, 0]),
        (5, [1, 1, 0, 0]),
        (6, [1, 0, 0, 0]),
    ]

    logger.info("\nTinder")
    tg = TinderGrouping()
    groups_tinder = tg.group_users(users_pref_like_third, [2, 2])
    for i, group in groups_tinder.items():
        logger.info(f"Group {i+1}: {group}")
