import datetime as dt
import multiprocessing

import pytz


def get_tw_time() -> str:
    tw = pytz.timezone("Asia/Taipei")
    twdt = tw.localize(dt.datetime.now()).strftime("%Y-%m-%d %H:%M:%S %Z%z")
    return twdt


def number_of_workers():
    print((multiprocessing.cpu_count() * 2) + 1)
    return (multiprocessing.cpu_count() * 2) + 1
