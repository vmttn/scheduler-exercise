from datetime import datetime

TIME_FN = datetime.utcnow


def get_time() -> datetime:
    return TIME_FN()
