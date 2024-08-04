__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import threading
from pylibcommons import libprint, libstopcontrol

class Thread(threading.Thread):
    def __init__(self, target, stop_callback = None, stop_control = libstopcontrol.StopControl(), args = [], kwargs = {}):
        assert isinstance(args, list), "args must be list for this object"
        self._stopped = False
        self._stopped_cond = threading.Condition()
        self._thread_stopped = False
        self._thread_target = target
        self._thread_cond = threading.Condition()
        self.stop_callback = stop_callback
        self.stop_control = stop_control
        self.stop_control.add(self)
        def _thread_target_wrapper(*args, **kwargs):
            _self = args[-1]
            try:
                _args = args[:-1]
                return _self._thread_target(*_args, **kwargs)
            finally:
                if _self.stop_callback and _self.is_stopped():
                    _self.stop_callback()
        args.append(self.get_stop_control())
        args.append(self)
        super().__init__(target = _thread_target_wrapper, args = args, kwargs = kwargs)
    def stop(self):
        with self._stopped_cond:
            self._stopped = True
            self._stopped_cond.notify_all()
    def wait_for_stop(self, timeout = None):
        with self._stopped_cond:
            if self._stopped is False:
                libprint.print_func_info()
                self._stopped_cond.wait(timeout = timeout)
    def is_stopped(self):
        with self._stopped_cond:
            return self._stopped
    def get_stop_control(self):
        return self.stop_control
