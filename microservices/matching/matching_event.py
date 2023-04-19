from typing import List, Tuple

from grouping_strategy import (
    GroupingStrategy,
    RandomGrouping,
    SimilarityGrouping,
    TinderGrouping,
)


class MatchingEventBuilder:
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.default_grouping_strategy: GroupingStrategy = RandomGrouping()
        self.grouping_strategy: GroupingStrategy = self.default_grouping_strategy
        self.group_size = 2
        self.slots = [2, 2, 2]

    def set_group_size(self, group_size: int):
        self.group_size = group_size
        return self

    def set_slot(self):
        # TODO: implement this
        raise NotImplementedError

    def set_strategy(self, grouping_strategy: str):
        if not isinstance(grouping_strategy, str):
            raise TypeError("grouping_strategy must be a string")

        if grouping_strategy == "random":
            self.grouping_strategy = RandomGrouping()
        elif grouping_strategy == "similarity":
            self.grouping_strategy = SimilarityGrouping()
        elif grouping_strategy == "tinder":
            self.grouping_strategy = TinderGrouping()
        else:
            self.grouping_strategy = self.default_grouping_strategy

        return self

    def match(self, users_pref: List[Tuple[int, List[int]]]) -> List[List[int]]:
        # TODO: validate self.slots
        # need more slots than unique uesrs

        # Divide the users into groups using a create_group function
        return self.grouping_strategy.group_users(users_pref, self.slots)


if __name__ == "__main__":
    # Define some example user data
    users_pref = [
        (1, [0, 1, 1, -1]),
        (2, [-1, 0, 1, -1]),
        (3, [1, -1, -1, 1]),
        (4, [-1, 1, 0, 1]),
        (5, [1, -1, -1, 1]),
    ]

    # Get the grouping strategy from the user
    strategy_choice = "random"

    # Create the matching event
    matching_event_builder = MatchingEventBuilder()

    # Group the users using the chosen strategy
    groups = matching_event_builder.set_strategy(strategy_choice).match(users_pref)

    for i, group in groups.items():
        print(f"Group {i+1}: {group}")

    # algorithm testing
    print("test")
    slots = [3, 3, 3]

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
