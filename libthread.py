__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import threading
from pylibcommons import libprint

class Thread(threading.Thread):
    def __init__(self, target, stop_callback = None, args = [], kwargs = {}):
        assert isinstance(args, list), "args must be list for this object"
        self._stopped = False
        self._stopped_cond = threading.Condition()
        self._thread_stopped = False
        self._thread_target = target
        self._thread_cond = threading.Condition()
        self.stop_callback = stop_callback
        def _thread_target_wrapper(*args, **kwargs):
            _self = args[-1]
            try:
                _args = args[:-1]
                return _self._thread_target(*_args, **kwargs)
            finally:
                with _self._thread_cond:
                    _self._thread_stopped = True
                    _self._thread_cond.notify_all()
        args.append(self.get_stop_control())
        args.append(self)
        super().__init__(target = _thread_target_wrapper, args = args, kwargs = kwargs)
    def stop(self):
        with self._stopped_cond:
            self._stopped = True
            self._stopped_cond.notify_all()
        self._wait_for_thread_end()
        if self.stop_callback:
            self.stop_callback()
    def wait_for_stop(self, timeout = None):
        with self._stopped_cond:
            if self._stopped is False:
                libprint.print_func_info()
                self._stopped_cond.wait(timeout = timeout)
    def is_stopped(self):
        with self._stopped_cond:
            return self._stopped
    def get_stop_control(self):
        return _StopControl(self)
    def _wait_for_thread_end(self):
        with self._thread_cond:
            while self._thread_stopped is False:
                self._thread_cond.wait()

class _StopControl:
    def __init__(self, thread_with_stop):
        self.thread_with_stop = thread_with_stop
    def wait_for_stop(self, timeout = None):
        self.thread_with_stop.wait_for_stop(timeout = timeout)
    def is_stopped(self):
        return self.thread_with_stop.is_stopped()
