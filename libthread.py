__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import threading
from pylibcommons import libprint, libstopcontrol

import logging
log = logging.getLogger(__name__)

def excepthook(exctype, value, tb, thread):
    libprint.print_exception(exctype, value, tb)
    libstopcontrol.stop_all()
    import sys
    sys.__excepthook__(exctype, value, tb)

class Thread(threading.Thread):
    def __init__(self, target, stop_callback = None, thread_name = None, stop_control = libstopcontrol.StopControl(), args = None, kwargs = None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        assert isinstance(args, list), "args must be list for this object"
        self._stopped = False
        self._stopped_cond = threading.Condition()
        self._thread_stopped = False
        self._thread_target = target
        self._thread_cond = threading.Condition()
        self.thread_name = thread_name
        self.stop_callback = stop_callback
        self.stop_control = stop_control
        self.stop_control.add(self)
        self.exception_info = None
        def _thread_target_wrapper(*args, **kwargs):
            _self = args[-1]
            try:
                _args = args[:-1]
                return _self._thread_target(*_args, **kwargs)
            except Exception as ex:
                _self.exception_info = (type(ex), ex, ex.__traceback__, _self)
            finally:
                if _self.stop_callback and _self.is_stopped():
                    _self.stop_callback()
        args.append(self.get_stop_control())
        args.append(self)
        super().__init__(target = _thread_target_wrapper, args = args, kwargs = kwargs)
    def start(self):
        libprint.print_func_info(logger = log.debug, extra_string = self.thread_name)
        super().start()
        libprint.print_func_info(logger = log.debug, extra_string = self.thread_name)
    def stop(self):
        libprint.print_func_info(logger = log.debug, extra_string = self.thread_name)
        with self._stopped_cond:
            self._stopped = True
            libprint.print_func_info(logger = log.debug, extra_string = self.thread_name)
            self._stopped_cond.notify_all()
        libprint.print_func_info(logger = log.debug, extra_string = self.thread_name)
    def wait_for_stop(self, timeout = None):
        libprint.print_func_info(logger = log.debug, extra_string = self.thread_name)
        with self._stopped_cond:
            if self._stopped is False:
                libprint.print_func_info(logger = log.debug, extra_string = self.thread_name)
                self._stopped_cond.wait(timeout = timeout)
        libprint.print_func_info(logger = log.debug, extra_string = self.thread_name)
    def is_stopped(self):
        libprint.print_func_info(logger = log.debug, extra_string = self.thread_name)
        with self._stopped_cond:
            return self._stopped
        libprint.print_func_info(logger = log.debug, extra_string = self.thread_name)
    def get_stop_control(self):
        return self.stop_control
    def join(self):
        libprint.print_func_info(logger = log.debug, extra_string = self.thread_name)
        super().join()
        if self.exception_info:
            exctype, value, tb, thread = self.exception_info
            import traceback
            traceback.print_tb(tb)
            if exctype is type(None):
                raise exctype
            if callable(exctype):
                raise exctype(value)
            raise exctype
        libprint.print_func_info(logger = log.debug, extra_string = self.thread_name)
