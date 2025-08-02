__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from pylibcommons import libprint, libthread
import logging
import threading

log = logging.getLogger(__name__)

import concurrent.futures as concurrent

class StopExecution:
    pass

def run(handler, address):
    return _Server(handler, address)

class _Server:
    def __init__(self, handler, address):
        libprint.print_func_info(prefix = "+", logger = log.info)
        self.lock = threading.Lock()
        self.cv = threading.Condition(self.lock)
        self.address = address
        from multiprocessing.connection import Listener
        try:
            self.listener = Listener(address)
            libprint.print_func_info(prefix = "*", logger = log.error, extra_string = f"Created listener. Address: {self.address}")
        except Exception as e:
            libprint.print_func_info(prefix = "*", logger = log.error, extra_string = f"Error creating listener: {e} Address: {self.address}")
            raise e
        self.thread = libthread.Thread(target = _Server.run_server, args = [self, handler, address])
        self.thread.start()
        libprint.print_func_info(prefix = "-", logger = log.info)
        self.stopped = False
    def stop(self):
        libprint.print_func_info(logger = log.info, extra_string = f"Stop server: {self.address}")
        if self.stopped:
            libprint.print_func_info(prefix = "*", logger = log.info, extra_string = f"Server already stopped: {self.address}")
            return
        self.stopped = True
        self.thread.get_stop_control().stop()
        from multiprocessing.connection import Client
        with Client(self.address) as client:
            client.close()
        self.listener.close()
        libprint.print_func_info(logger = log.info, extra_string = f"Listener stopped {self.address}")
    def wait_for_finish(self):
        self.thread.join()
    @staticmethod
    def run_server(self, handler, address, stop_control):
        libprint.print_func_info(prefix = "+", logger = log.info)
        try:
            def call(callback):
                if callback is not None and callable(callback):
                    callback()
            def thread_client(client, self):
                libprint.print_func_info(prefix = "+", logger = log.debug, extra_string = f"Create client: {client}")
                try:
                    while not stop_control.is_stopped():
                        libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = f"+client {client}.recv")
                        line = None
                        try:
                            line = client.recv()
                        except EOFError as eof:
                            libprint.print_func_info(prefix = "*", logger = log.info, extra_string = f"Received eof: {eof}")
                            return
                        libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = f"-client {client}.recv")
                        output = handler(line, client)
                        if isinstance(output, StopExecution) or output == StopExecution:
                            libprint.print_func_info(prefix = "*", logger = log.info, extra_string = "Stop execution")
                            self.stop()
                            return output
                except EOFError as eof:
                    libprint.print_func_info(prefix = "*", logger = log.error, extra_string = f"{eof}")
                finally:
                    client.close()
                    libprint.print_func_info(prefix = "-", logger = log.info, extra_string = f"{client}")
            with concurrent.ThreadPoolExecutor() as executor:
                futures = []
                while not stop_control.is_stopped():
                    libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = f"+listener.accept")
                    conn = self.listener.accept()
                    if stop_control.is_stopped(): break
                    libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = f"-listener.accept")
                    futures.append(executor.submit(thread_client, conn, self))
                    libprint.print_func_info(prefix = "*", logger = log.debug, extra_string = f"futures count: {len(futures)}")
                for f in futures: f.result()
        finally:
            libprint.print_func_info(prefix = "-", logger = log.info, print_thread_id = True)
