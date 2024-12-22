__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import concurrent.futures as concurrent
import threading

class StopControl:
    def __init__(self):
        self.threads_with_stop = []
        self.lock = threading.RLock()
        self._executor = None
    def add(self, thread):
        def check(thread):
            if not hasattr(thread, "stop"):
                raise Exception("thread must have stop method")
            if not hasattr(thread, "wait_for_stop"):
                raise Exception("thread must have wait_for_stop method")
            if not hasattr(thread, "is_stopped"):
                raise Exception("thread must have is_stopped method")
        check(thread)
        with self.lock:
            self.threads_with_stop.append(thread)
    def wait_for_stop(self, timeout = None):
        tws = []
        with self.lock:
            tws = self.threads_with_stop.copy()
        for thread in tws:
            thread.wait_for_stop(timeout = timeout)
    def is_stopped(self):
        tws = []
        with self.lock:
            tws = self.threads_with_stop.copy()
        for thread in tws:
            if thread.is_stopped() is False:
                return False
        return True
    def stop(self):
        def stop_single(self, index):
            thread = None
            with self.lock:
                thread = self.threads_with_stop[index]
            thread.stop()
        if self._executor is None:
            self._executor = concurrent.ThreadPoolExecutor(max_workers = len(self.threads_with_stop))
        futures = [self._executor.submit(stop_single, self, index) for index, t in enumerate(self.threads_with_stop)]
        for future in futures: future.result()
