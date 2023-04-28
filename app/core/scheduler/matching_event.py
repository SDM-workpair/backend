from sqlalchemy import event
import loguru
from app.models.matching_room import MatchingRoom
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from tzlocal import get_localzone


"""
Matching event scheduler
"""
scheduler = BackgroundScheduler()
scheduler.start()

def matching_event(matching_room: MatchingRoom):
    loguru.logger.info("run matching_event function")
    return

def schedule_matching_event(matching_room: MatchingRoom):
    loguru.logger.info(matching_room)
    # call matching_event function
    due_time = matching_room.due_time
    scheduler.add_job(
        matching_event,
        'date',
        run_date=due_time,
        args=[matching_room]
    )
    return


@event.listens_for(MatchingRoom, 'after_insert')
def schedule_matching_room(mapper, connection, matching_room):
    "listen for the 'after_insert' event"
    schedule_matching_event(matching_room=matching_room)
    

@atexit.register
def shutdown_scheduler():
    scheduler.shutdown()
