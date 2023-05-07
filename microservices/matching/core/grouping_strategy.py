import random
from abc import ABC, abstractmethod
from typing import List, Tuple

from numpy import dot, linalg, zeros


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
        popularity = sorted(users, key=lambda x: sum(x[1]), reverse=True)

        while users_left:
            leader = None
            for user in popularity:
                if user in users_left:
                    leader = user
                    break

            group_size = min(len(users_left), slots[group_index])
            group = [leader[0]]
            users_left.remove(leader)

            while len(group) < group_size and users_left:
                candidate = None
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

        # Randomly assign users to groups
        while users_left:
            group_index = random.randint(0, num_groups - 1)
            if len(groups[group_index]) < slots[group_index]:
                user = users_left.pop(0)
                groups[group_index].append(user[0])
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
        (1, [0, 1, 1, -1]),
        (2, [-1, 0, 1, -1]),
        (3, [1, -1, -1, 1]),
        (4, [-1, 1, 0, 1]),
        (5, [1, -1, -1, 1]),
    ]

    # algorithm testing
    print("test")
    slots = [3, 2, 1]

    print("Tinder")
    tg = TinderGrouping()
    groups_tinder = tg.group_users(users_pref, slots)

    for i, group in groups_tinder.items():
        print(f"Group {i+1}: {group}")

    print("Random")
    rg = RandomGrouping()
    groups_random = rg.group_users(users_pref, slots)

    for i, group in groups_random.items():
        print(f"Group {i+1}: {group}")

    print("Similarity")
    sg = SimilarityGrouping()
    groups = sg.group_users(users_pref, slots)

    for i, group in groups.items():
        print(f"Group {i+1}: {group}")
