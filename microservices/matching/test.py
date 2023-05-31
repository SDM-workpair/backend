# from fastapi.testclient import TestClient


# from .main import app  # Flask instance of the API

# client = TestClient(app)


# def test_matching_healthchecker():
#     response = client.get("/healthchecker")
#     assert response.status_code == 200


# def test_create_matching_event_test():
#     data = {
#         "room_id": "test",
#         "group_choice": "random",
#         "slot_choice": "fixed_group",
#         "params": {"num_groups": 3},
#     }

#     response = client.post("/matching/create/test", json=data)
#     assert response.status_code == 200

#     response = client.post("/matching/create/test")
#     assert response.status_code == 422


# def test_slot_generator():
#     sg = FixedGroupSlot().set_num_users(10)

#     desired_slots = [
#         [5, 5],
#         [4, 3, 3],
#         [3, 3, 2, 2],
#         [2, 2, 2, 2, 2],
#         [2, 2, 2, 2, 1, 1],
#     ]
#     # Generate slots with fixed group amount
#     for num_groups, desire in zip([2, 3, 4, 5, 6], desired_slots):
#         slot_params = {"num_groups": num_groups}
#         slots = sg.generate_slots(params=slot_params)
#         assert slots == desire

#     # Generate slots with fixed max/min users
#     generator = MaxUserSlot().set_num_users(10)
#     slot_params = {"min_users": 2, "max_users": 4}
#     slots = generator.generate_slots(params=slot_params)
#     assert slots == [4, 4]

#     # Generate slots with fixed max/min users
#     generator = MinUserSlot().set_num_users(10)
#     slot_params = {"min_users": 2}
#     slots = generator.generate_slots(params=slot_params)

#     assert slots == [2, 2, 2, 2, 2]


# def test_matching_event():
#     small_data = [
#         (1, [0, 1, 1, -1, 1]),
#         (2, [-1, 0, 1, -1, 1]),
#         (3, [1, -1, -1, 1, 1]),
#         (4, [-1, 1, 0, 1, 1]),
#         (5, [1, -1, 1, 1, 1]),
#         (6, [1, 0, -1, 1, 1]),
#         (7, [1, -1, -1, 1, 1]),
#         (8, [1, -1, -1, 1, 1]),
#         (9, [1, -1, -1, 1, 1]),
#         (10, [1, -1, -1, 1, 1]),
#         (11, [1, -1, -1, 1, 1]),
#     ]
#     # Define some example user data
#     test_config = [
#         {
#             "group_choice": "tinder",
#             "slot_choice": "fixed_group",
#             "params": {"num_groups": 3},
#             "users_pref": small_data,
#         },
#         {
#             "group_choice": "tinder",
#             "slot_choice": "fixed_min",
#             "params": {"max_users": 5, "min_users": 4},
#             "users_pref": small_data,
#         },
#         {
#             "group_choice": "similarity",
#             "slot_choice": "fixed_max",
#             "params": {"max_users": 5, "min_users": 4},
#             "users_pref": small_data,
#         },
#         {
#             "group_choice": "tinder",
#             "slot_choice": "fixed_group",
#             "params": {"num_groups": 3},
#             "users_pref": small_data,
#         },
#         {
#             "group_choice": "tinder",
#             "slot_choice": "fixed_min",
#             "params": {"max_users": 5, "min_users": 2},
#             "users_pref": small_data,
#         },
#         {
#             "group_choice": "similarity",
#             "slot_choice": "fixed_max",
#             "params": {"max_users": 5, "min_users": 2},
#             "users_pref": small_data,
#         },
#     ]

#     desired_groups = [
#         [[5, 1, 4, 6], [3, 7, 8, 9], [10, 11, 2]],
#         [[5, 1, 4, 6, 10, 11, 2], [3, 7, 8, 9]],
#         [[1, 2, 4, 5, 6], [3, 7, 9, 10, 11]],
#         [[5, 1, 4, 6], [3, 7, 8, 9], [10, 11, 2]],
#         [
#             [5, 1, 2],
#             [4, 6],
#             [3, 7],
#             [8, 9],
#             [10, 11],
#         ],
#         [
#             [1, 2, 4, 5, 6],
#             [3, 7, 9, 10, 11],
#         ],
#     ]
#     for config, desire_groups in zip(test_config, desired_groups):
#         # Create the matching event
#         matching_event_builder = OneTimeMatchingEventBuilder()

#         # Group the users using the chosen strategy
#         groups = (
#             matching_event_builder.set_total_users(len(config["users_pref"]))
#             .set_strategy(config["group_choice"], config["slot_choice"])
#             .set_slot_params(config["params"])
#             .match(config["users_pref"])
#         )

#         for (i, group), desire in zip(groups.items(), desire_groups):
#             # print(f"Group {i+1}: {group}, {desire}")
#             # print(group , ",")
#             assert group == desire
