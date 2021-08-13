from datetime import datetime

from dateutil import tz


def get_tz_time() -> datetime:
    return datetime.now(tz=tz.tzlocal())


DEFAULT_TIME_FN = get_tz_time


def get_time() -> datetime:
    return DEFAULT_TIME_FN()
