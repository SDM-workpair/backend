from abc import ABC, abstractmethod
from typing import Dict, List


class SlotGenerator(ABC):
    def __init__(self):
        self.num_users = 1

    @abstractmethod
    def generate_slots(self, params: Dict[str, int]) -> List[int]:
        pass

    def set_num_users(self, num_users: int):
        self.num_users = num_users

    def set_proximity(self, proximity):
        self.proximity = proximity

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
            max_users = params["max_users"]
            assert (
                max_users < self.num_users
            ), "max_users must be less than total users"  # ??
        except ValueError:
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
            assert (
                min_users <= self.num_users
            ), "min_users must be less than total users"
        except ValueError:
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


class FixedMaxMinSlot(SlotGenerator):
    def __init__(self):
        super().__init__()


#     def generate_slots(self, params: Dict[str, int]) -> List[int]:
#         try:
#             min_users = max(params["min_users"], 1)
#             max_users = params["max_users"]
#             assert (
#                 min_users <= max_users
#             ), "min_users must be less than or equal to max_users"
#             assert (
#                 min_users <= self.num_users
#             ), "min_users must be less than or equal to the total number of users"
#         except ValueError:
#             raise ValueError(
#                 "min_users and max_users must be specified for fixed max/min strategy"
#             )

#         # calculate the target group size
#         target_size = max_users
#         num_groups = self.num_users // target_size

#         # distribute remaining users to groups that are below the target size
#         remaining_users = self.num_users - (num_groups * target_size)
#         if remaining_users > 0:
#             slots = [target_size for _ in range(num_groups)]
#             while remaining_users > 0:
#                 for i in range(len(slots)):
#                     if remaining_users == 0:
#                         break
#                     if slots[i] < max_users:
#                         slots[i] += 1
#                         remaining_users -= 1
#             if remaining_users > 0:
#                 slots.append(remaining_users)
#         else:
#             slots = [target_size for _ in range(num_groups)]

#         # adjust group size to meet the min/max requirements
#         for i in range(len(slots)):
#             if slots[i] < min_users:
#                 slots[i] = min_users
#             elif slots[i] > max_users:
#                 slots[i] = max_users

#         return slots


if __name__ == "__main__":
    sg = FixedGroupSlot(7)

    # Generate slots with fixed group amount
    for num_groups in [2, 3, 4, 5, 6]:
        slot_params = {"num_groups": num_groups}
        slots = sg.generate_slots(params=slot_params)
        print(f"Fixed group amount: {num_groups} -> {slots}")

    # Generate slots with fixed max/min users
    generator = FixedMaxMinSlot(7)
    slot_params = {"min_users": 2, "max_users": 4}
    slots = generator.generate_slots(params=slot_params)
    print(
        f"Fixed max min: {slot_params['max_users']}/{slot_params['min_users']} -> {slots}"
    )

    # Generate slots with fixed max/min users
    generator = FixedMaxMinSlot(7)
    slot_params = {"min_users": 2, "max_users": 3}
    slots = generator.generate_slots(params=slot_params)
    print(
        f"Fixed max min: {slot_params['max_users']}/{slot_params['min_users']} -> {slots}"
    )
