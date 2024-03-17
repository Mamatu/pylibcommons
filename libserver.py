from pylibcommons import libprint, libprocess, libkw
import logging
import os
import threading

log = logging.getLogger(__name__)

import concurrent.futures as concurrent

class StopExecution:
    pass

def run(handler, address):
    return _Server(handler, address)

class _Server:
    def __init__(self, handler, address):
        libprint.print_func_info(prefix = "+", logger = log.debug)
        self.lock = threading.Lock()
        self.cv = threading.Condition(self.lock)
        self.address = address
        self.stopped = False
        from multiprocessing.connection import Listener
        self.listener = Listener(address)
        self.thread = threading.Thread(target = _Server.run_server, args = [self, handler, address])
        self.thread.daemon = True
        self.thread.start()
        libprint.print_func_info(prefix = "-", logger = log.debug)
    def stop(self):
        self.stopped = True
        from multiprocessing.connection import Client
        client = Client(self.address)
        client.close()
    def wait_for_finish(self):
        with self.cv:
            while not self.stopped:
                self.cv.wait()
    @staticmethod
    def run_server(self, handler, address):
        libprint.print_func_info(prefix = "+", logger = log.debug)
        try:
            def call(callback):
                if callback is not None and callable(callback):
                    callback()
            def thread_client(client, self):
                libprint.print_func_info(prefix = "+", logger = log.debug, extra_string = f"{client}")
                try:
                    while not self.stopped:
                        libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = f"+client {client}.recv")
                        line = client.recv()
                        libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = f"-client {client}.recv")
                        output = handler(line, client)
                        if isinstance(output, StopExecution) or output == StopExecution:
                            libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = f"Stop execution")
                            return
                except EOFError as eof:
                    libprint.print_func_info(prefix = "*", logger = log.error, extra_string = f"{eof}")
                finally:
                    client.close()
                    libprint.print_func_info(prefix = "-", logger = log.debug, extra_string = f"{client}")
            with concurrent.ThreadPoolExecutor() as executor:
                futures = []
                while not self.stopped:
                    libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = "+listener.accept")
                    conn = self.listener.accept()
                    if self.stopped: break
                    libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = "-listener.accept")
                    futures.append(executor.submit(thread_client, conn, self))
                for f in futures: f.result()
        finally:
            libprint.print_func_info(prefix = "-", logger = log.debug)
