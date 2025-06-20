__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import threading
import time

class TimeoutException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
    def __str__(self):
        return self.message

def while_with_timeout(timeout, condition, timeout_msg = None, time_sleep = 0.1):
    start_time = time.time()
    timeouted = False
    while True:
        status = condition()
        output = None
        if isinstance(status, tuple):
            status = status[0]
            output = status[1]
        if not status:
            return output
        time_time = time.time()
        if time_time - start_time >= timeout:
            timeouted = True
            break
        if time_time + time_sleep > start_time + timeout:
            time_sleep = (start_time + timeout) - time_time
        time.sleep(time_sleep)
    if timeouted:
        if timeout_msg is None:
            timeout_msg = "Timeout in while"
        raise TimeoutException(timeout_msg)
