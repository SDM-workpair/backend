from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from grouping_strategy import (
    GroupingStrategy,
    RandomGrouping,
    SimilarityGrouping,
    TinderGrouping,
)
from slot_generator import FixedGroupSlot, FixedMaxMinSlot, SlotGenerator


class MatchingEventBuilder(ABC):
    def __init__(self):
        self.default_grouping_strategy: GroupingStrategy = RandomGrouping()
        self.default_slot_strategy: SlotGenerator = FixedGroupSlot
        self.group_size = 2
        self.slots = [2, 2, 2]

    @abstractmethod
    def set_group_size(self):
        return NotImplementedError

    @abstractmethod
    def set_strategy(self):
        return NotImplementedError


class ContinueMatchingEventBuilder(MatchingEventBuilder):
    def __init__():
        pass


class OneTimeMatchingEventBuilder(MatchingEventBuilder):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.grouping_strategy: GroupingStrategy = self.default_grouping_strategy
        self.slot_generator: SlotGenerator = None
        self.slots = []
        self.total_users = 1

    def set_group_size(self, group_size: int):
        self.group_size = group_size
        return self

    def set_slot_params(self, params: Dict[str, int]):
        self.slot_params = params
        return self

    def set_total_users(self, total_users):
        self.total_users = total_users
        return self

    def set_strategy(self, grouping_strategy: str, slot_strategy: str):
        if not isinstance(grouping_strategy, str):
            raise TypeError("grouping_strategy must be a string")
        if not isinstance(slot_strategy, str):
            raise TypeError("slot_strategy must be a string")

        # set grouping strategy
        if grouping_strategy == "random":
            self.grouping_strategy = RandomGrouping()
        elif grouping_strategy == "similarity":
            self.grouping_strategy = SimilarityGrouping()
        elif grouping_strategy == "tinder":
            self.grouping_strategy = TinderGrouping()
        else:
            self.grouping_strategy = self.default_grouping_strategy

        # set slot strategy
        if slot_strategy == "fixed_group_amount":
            self.slot_generator = FixedGroupSlot()
        elif slot_strategy == "fixed_max_min":
            self.slot_generator = FixedMaxMinSlot()
        else:
            self.slot_generator = FixedGroupSlot()
        return self

    def set_slot_proximity(self, proximity: bool):
        self.slot_generator.set_proximity(proximity)
        return self

    def match(self, users_pref: List[Tuple[int, List[int]]]) -> List[List[int]]:
        self.slot_generator.set_num_users(self.total_users)
        self.slots = self.slot_generator.generate_slots(self.slot_params)
        # Divide the users into groups using a create_group function

        return self.grouping_strategy.group_users(users_pref, self.slots)


if __name__ == "__main__":
    import os.path
    import random

    # check if file exist in directory
    if not os.path.isfile("data.txt"):
        # Generate a list of tuples with random data
        data = []
        for i in range(0, 200):
            data.append(tuple([i, [random.randint(-1, 1) for _ in range(200)]]))

        # Write the list to a file
        with open("data.txt", "w") as f:
            for item in data:
                f.write("%s,\n" % str(item))

    def read_data(filename):
        data = []
        with open(filename, "r") as f:
            for line in f:
                # Remove trailing comma and newline characters
                line = line.strip(",\n")
                # Convert string to tuple and append to list
                data.append(eval(line))
        return data

    large_data = read_data("data.txt")
    small_data = [
        (1, [0, 1, 1, -1, 1]),
        (2, [-1, 0, 1, -1, 1]),
        (3, [1, -1, -1, 1, 1]),
        (4, [-1, 1, 0, 1, 1]),
        (5, [1, -1, 1, 1, 1]),
        (6, [1, 0, -1, 1, 1]),
        (7, [1, -1, -1, 1, 1]),
        (7, [1, -1, -1, 1, 1]),
        (7, [1, -1, -1, 1, 1]),
        (7, [1, -1, -1, 1, 1]),
        (7, [1, -1, -1, 1, 1]),
    ]
    # Define some example user data
    test_config = [
        {
            "group_choice": "random",
            "slot_choice": "fixed_group_amount",
            "params": {"num_groups": 3},
            "users_pref": small_data,
        },
        {
            "group_choice": "tinder",
            "slot_choice": "fixed_max_min",
            "params": {"max_users": 4, "min_users": 0},
            "users_pref": small_data,
        },
        {
            "group_choice": "similarity",
            "slot_choice": "fixed_max_min",
            "params": {"max_users": 5, "min_users": 4},
            "users_pref": small_data,
        },
        {
            "group_choice": "random",
            "slot_choice": "fixed_group_amount",
            "params": {"num_groups": 3},
            "users_pref": large_data,
        },
        {
            "group_choice": "tinder",
            "slot_choice": "fixed_max_min",
            "params": {"max_users": 5, "min_users": 2},
            "users_pref": large_data,
        },
        {
            "group_choice": "similarity",
            "slot_choice": "fixed_max_min",
            "params": {"max_users": 5, "min_users": 2},
            "users_pref": large_data,
        },
    ]

    for config in test_config:
        print(
            f"group_choice: {config['group_choice']}, slot_choice: {config['slot_choice']}"
        )
        # Create the matching event
        matching_event_builder = OneTimeMatchingEventBuilder()

        # Group the users using the chosen strategy
        groups = (
            matching_event_builder.set_total_users(len(config["users_pref"]))
            .set_strategy(config["group_choice"], config["slot_choice"])
            .set_slot_params(config["params"])
            .match(config["users_pref"])
        )

        for i, group in groups.items():
            print(f"Group {i+1}: {group}")
