import os
from datetime import datetime

TIME_FORMAT = '%Y/%m/%d %H:%M:%S'


def fetch_file_updated_time(path):
    timestamp = os.path.getmtime(path)
    return datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)


def fetch_now_time():
    return datetime.now().strftime((TIME_FORMAT))
