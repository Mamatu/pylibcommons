import concurrent.futures as concurrent

class StopControl:
    def __init__(self):
        self.threads_with_stop = []
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
        self.threads_with_stop.append(thread)
    def wait_for_stop(self, timeout = None):
        for thread in self.threads_with_stop:
            thread.wait_for_stop(timeout = timeout)
    def is_stopped(self):
        for thread in self.threads_with_stop:
            if thread.is_stopped() is False:
                return False
        return True
    def stop(self):
        def stop_single(self, index):
            self.threads_with_stop[index].stop()
        if self._executor is None:
            self._executor = concurrent.ThreadPoolExecutor(max_workers = len(self.threads_with_stop))
        futures = [self._executor.submit(stop_single, self, index) for index, t in enumerate(self.threads_with_stop)]
        for future in futures: future.result()
