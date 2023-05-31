"""
This is an example showing how to make the scheduler into a remotely accessible service.
It uses RPyC to set up a service through which the scheduler can be made to add, modify and remove
jobs.

To run, first install RPyC using pip. Then change the working directory to the ``rpc`` directory
and run it with ``python -m server``.
"""

from time import sleep

import rpyc
from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger
from rpyc.utils.server import ThreadedServer


# server
def print_text(text):
    logger.info(text)


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
        SchedulerService, port=12345, protocol_config=protocol_config
    )
    try:
        server.start()
        # client
        conn = rpyc.connect("localhost", 12345)
        job = conn.root.add_job(
            "print_text", "interval", args=["Hello, World"], seconds=2
        )
        sleep(10)
        conn.root.remove_job(job.id)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()
