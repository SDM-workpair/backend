from sqlalchemy import event
import loguru
# from models.matching_room import MatchingRoom

"""
Matching event scheduler
"""

# 監聽 DB: receive_after_insert
# 存到一個queue
# 放到FastAPI scheduler


# @event.listens_for(MatchingRoom, 'after_insert')
# def receive_after_insert(mapper, connection, target):
#     "listen for the 'after_insert' event"
#     loguru.logger.info(mapper)
#     loguru.logger.info(connection)
#     loguru.logger.info(target.due_time)
    

#     # ... (event handling logic) ...

def matching_event(time: str):
    loguru.logger.info(time)
    return