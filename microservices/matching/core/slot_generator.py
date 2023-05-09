from abc import ABC, abstractmethod
from typing import Dict, List

from loguru import logger


class SlotGenerator(ABC):
    def __init__(self):
        self.num_users = 1
        self.proximity = False

    @abstractmethod
    def generate_slots(self, params: Dict[str, int]) -> List[int]:
        pass

    def set_num_users(self, num_users: int):
        self.num_users = num_users
        return self

    def set_proximity(self, proximity: bool):
        self.proximity = proximity
        return self

    def divide_users_to_group(self, num_groups: int):
        group_size = self.num_users // num_groups
        num_larger_groups = self.num_users % num_groups
        slots = [
            group_size + 1 if i < num_larger_groups else group_size
            for i in range(num_groups)
        ]
        return slots


class FixedGroupSlot(SlotGenerator):
    def __init__(self):
        super().__init__()

    def generate_slots(self, params: Dict[str, int]) -> List[int]:
        try:
            num_groups = params["num_groups"]
            assert (
                num_groups <= self.num_users
            ), "num_groups must be less than or equal to the total number of users"
        except Exception:
            logger.error("num_groups must be specified for fixed group amount strategy")
            raise ValueError(
                "num_groups must be specified for fixed group amount strategy"
            )

        slots = self.divide_users_to_group(num_groups)

        return slots


class MaxUserSlot(SlotGenerator):
    def __init__(self):
        super().__init__()

    def generate_slots(self, params: Dict[str, int]) -> List[int]:
        try:
            max_users = min(params["max_users"], self.num_users)
        except ValueError as e:
            logger.error(f"max_users must be specified for fixed max strategy, {e}")
            raise ValueError("max_users must be specified for fixed max strategy")

        num_groups = self.num_users // max_users
        remaining_users = self.num_users - (num_groups * max_users)
        slots = [max_users for _ in range(num_groups)]

        if remaining_users == 0:
            return slots

        if self.proximity:
            # distribute remaining users to groups that are closest to the target size
            groups = len(slots) + 1
            slots = self.divide_users_to_group(groups)

        return slots


class MinUserSlot(SlotGenerator):
    def __init__(self):
        super().__init__()

    def generate_slots(self, params: Dict[str, int]) -> List[int]:
        try:
            min_users = max(params["min_users"], 1)
            min_users = min(min_users, self.num_users)
            assert (
                min_users <= self.num_users
            ), "min_users must be less than total users"
        except ValueError as e:
            logger.error(f"min_users must be specified for fixed min strategy, {e}")
            raise ValueError("min_users must be specified for fixed min strategy")

        num_groups = self.num_users // min_users
        remaining_users = self.num_users - (num_groups * min_users)
        slots = [min_users for _ in range(num_groups)]

        if remaining_users == 0:
            return slots

        if self.proximity:
            # distribute remaining users to groups that are closest to the target size
            groups = len(slots)
            slots = self.divide_users_to_group(groups)

        return slots


if __name__ == "__main__":
    sg = FixedGroupSlot().set_num_users(10)

    # Generate slots with fixed group amount
    for num_groups in [2, 3, 4, 5, 6]:
        slot_params = {"num_groups": num_groups}
        slots = sg.generate_slots(params=slot_params)
        print(f"Fixed group amount: {num_groups} -> {slots}")

    # Generate slots with fixed max/min users
    generator = MaxUserSlot().set_num_users(10)
    slot_params = {"min_users": 2, "max_users": 4}
    slots = generator.generate_slots(params=slot_params)
    print(f"Fixed max: {slot_params['max_users']} -> {slots}")

    # Generate slots with fixed max/min users
    generator = MinUserSlot().set_num_users(10)
    slot_params = {"min_users": 2}
    slots = generator.generate_slots(params=slot_params)
    print(f"Fixed min: {slot_params['min_users']} -> {slots}")
