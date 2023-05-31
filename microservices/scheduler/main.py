import sys
import traceback

import rpyc
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from loguru import logger
from rpyc.utils.server import ThreadedServer

from microservices.matching.schema import MatchingEvent, Message
from microservices.scheduler.database import SessionLocal

app = FastAPI()

base_response = {
    500: {"model": Message},
    404: {"model": Message},
    501: {"model": Message},
}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/scheduler/create/test")
def create_matching_event_test(config: MatchingEvent):
    """Create test matching event"""

    logger.info("invoke mathcing event create")

    return {"message": "success"}


@app.get("/healthchecker")
def healthchecker():
    return {"msg": "Scheduler Service is running"}


def getexception(e):
    error_class = e.__class__.__name__  # 取得錯誤類型
    detail = e.args[0]  # 取得詳細內容
    cl, exc, tb = sys.exc_info()  # 取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
    fileName = lastCallStack[0]  # 取得發生的檔案名稱
    lineNum = lastCallStack[1]  # 取得發生的行號
    funcName = lastCallStack[2]  # 取得發生的函數名稱

    errMsg = 'File "{}", line {}, in {}: [{}] {}'.format(
        fileName, lineNum, funcName, error_class, detail
    )
    print(errMsg)


"""
This is an example showing how to make the scheduler into a remotely accessible service.
It uses RPyC to set up a service through which the scheduler can be made to add, modify and remove
jobs.

To run, first install RPyC using pip. Then change the working directory to the ``rpc`` directory
and run it with ``python -m server``.
"""


def print_text(text):
    print(text)


class SchedulerService(rpyc.Service):
    def exposed_add_job(self, func, *args, **kwargs):
        return scheduler.add_job(func, *args, **kwargs)

    def exposed_modify_job(self, job_id, jobstore=None, **changes):
        return scheduler.modify_job(job_id, jobstore, **changes)

    def exposed_reschedule_job(
        self, job_id, jobstore=None, trigger=None, **trigger_args
    ):
        return scheduler.reschedule_job(job_id, jobstore, trigger, **trigger_args)

    def exposed_pause_job(self, job_id, jobstore=None):
        return scheduler.pause_job(job_id, jobstore)

    def exposed_resume_job(self, job_id, jobstore=None):
        return scheduler.resume_job(job_id, jobstore)

    def exposed_remove_job(self, job_id, jobstore=None):
        scheduler.remove_job(job_id, jobstore)

    def exposed_get_job(self, job_id):
        return scheduler.get_job(job_id)

    def exposed_get_jobs(self, jobstore=None):
        return scheduler.get_jobs(jobstore)


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.start()
    logger.info(f"scheduler is running:  {scheduler.running}")
    protocol_config = {"allow_public_attrs": True}
    server = ThreadedServer(
        SchedulerService, port=8003, protocol_config=protocol_config
    )
    try:
        server.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()
