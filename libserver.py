from pylibcommons import libprint, libprocess, libkw
import logging
import os
import threading

log = logging.getLogger(__name__)

class StopExecution:
    pass

def run(handler, port, server_before_accept = None, server_finished = None):
    return _Server(handler, port, server_before_accept, server_finished)

class _Server:
    def __init__(self, handler, port, server_before_accept = None, server_finished = None):
        libprint.print_func_info(prefix = "+", logger = log.debug)
        self.lock = threading.Lock()
        self.cv = threading.Condition(self.lock)
        self.thread = threading.Thread(target = _Server.run_server, args = [self, handler, port, server_before_accept, server_finished])
        self.thread.daemon = True
        self.thread.start()
        self.stopped = False
        libprint.print_func_info(prefix = "-", logger = log.debug)
    def wait_for_finish(self):
        with self.cv:
            while not self.stopped:
                self.cv.wait()
    @staticmethod
    def run_server(self, handler, port, server_before_accept = None, server_finished = None):
        libprint.print_func_info(prefix = "+", logger = log.debug)
        from multiprocessing.connection import Listener
        address = ('localhost', port)
        listener = Listener(address)
        def call(callback):
            if callback is not None and callable(callback):
                callback()
        call(server_before_accept)
        libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = "+listener.accept")
        conn = listener.accept()
        libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = "-listener.accept")
        try:
            while True:
                libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = "+conn.recv")
                line = conn.recv()
                libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = "-conn.recv")
                output = handler(line)
                if isinstance(output, StopExecution) or output == StopExecution:
                    libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = f"Stop execution")
                    return
        finally:
            conn.close()
            with self.cv:
                self.stopped = True
                self.cv.notify()
            call(server_finished)
            libprint.print_func_info(prefix = "-", logger = log.debug)
