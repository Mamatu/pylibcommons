__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import logging
log = logging.getLogger(__name__)

from pylibcommons import  libkw, libprint, libthread, libstopcontrol
import threading
import traceback

import multiprocessing as mp
import concurrent.futures as concurrent

def schedule_jobs(processes, jobs_count, process_filter = lambda process: process, **kwargs):
    def target(lock, index, processes, process_filter, print_stderr, print_stdout, exception_on_error, stop_on_exception, log, exceptions, stop_control):
        while not stop_control.is_stopped():
            try:
                with lock:
                    idx = index[0]
                    index[0] = index[0] + 1
                if idx >= len(processes):
                    return
                process = process_filter(processes[idx])
                process.start()
                wait_kwargs = {}
                wait_kwargs["print_stderr"] = print_stderr
                wait_kwargs["print_stdout"] = print_stdout
                wait_kwargs["exception_on_error"] = exception_on_error
                process.wait(**wait_kwargs)
            except Exception as ex:
                tb = traceback.format_exc()
                libprint.print_func_info(logger = log.error, extra_string = f"{ex}\n{tb}")
                with lock:
                    exceptions.append((ex, tb))
                if stop_on_exception:
                    stop_control.stop()
                    return
    print_stderr = libkw.handle_kwargs("print_stderr", default_output = False, **kwargs)
    print_stdout = libkw.handle_kwargs("print_stdout", default_output = False, **kwargs)
    exception_on_error = libkw.handle_kwargs("exception_on_error", default_output = True, **kwargs)
    stop_on_exception = libkw.handle_kwargs("stop_on_exception", default_output = True, **kwargs)
    threads = []
    exceptions = []
    lock = threading.Lock()
    index = [0]
    stop_control = libstopcontrol.StopControl()
    args_list = [lock, index, processes, process_filter, print_stderr, print_stdout, exception_on_error, stop_on_exception, log, exceptions]
    for i in range(jobs_count):
        thread_name = f"scheduled job {i}"
        threads.append(libthread.Thread(stop_control = stop_control, args = args_list.copy(), target = target, thread_name = thread_name))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return exceptions

def schedule_jobs_threads(processes, jobs_count, process_filter = lambda process: process, **kwargs):
    return schedule_jobs(processes, jobs_count, process_filter = process_filter, **kwargs)

class ProcessException(Exception):
    def __init__(self, message, process, tb):
        super().__init__(message)
        self.process = process
        self.tb = tb

def handle_recv(parent_conn):
    while True:
        output = parent_conn.recv()
        if output is None:
            break
        if isinstance(output, str):
            print(f"Process name: {output}")
            libprint.print_func_info(logger = log.info, extra_string = f"Process name: {output}")
        if isinstance(output, ProcessException):
            ex = output
            tb = ex.tb
            print(f"Process exception: {ex}\n{tb}")
            libprint.print_func_info(logger = log.info, extra_string = f"Process exception: {ex}\n{tb}")

def schedule_jobs_multiprocesses(processes, jobs_count, process_filter = lambda process: process, **kwargs):
    def target(lock, index, processes, process_filter, print_stderr, print_stdout, exception_on_error, stop_on_exception, log, exceptions, stop_control, thread_name, child_conn):
        try:
            child_conn.send(thread_name)
            is_stopped = stop_control.is_stopped()
            while not stop_control.is_stopped():
                with lock:
                    idx = index[0]
                    index[0] = index[0] + 1
                if idx >= len(processes):
                    return
                child_conn.send(f"Processing index {idx} of {len(processes)}")
                process = process_filter(processes[idx])
                process.start()
                wait_kwargs = {}
                wait_kwargs["print_stderr"] = print_stderr
                wait_kwargs["print_stdout"] = print_stdout
                wait_kwargs["exception_on_error"] = exception_on_error
                process.wait(**wait_kwargs)
        except Exception as ex:
            tb = traceback.format_exc()
            pe = ProcessException(f"Exception in process {process}", process, tb)
            child_conn.send(pe)
            with lock:
                exceptions.append((ex, tb))
            if stop_on_exception:
                stop_control.stop()
                return
        finally:
            child_conn.send(None)  # Send None to indicate completion
            child_conn.close()
    print_stderr = libkw.handle_kwargs("print_stderr", default_output = False, **kwargs)
    print_stdout = libkw.handle_kwargs("print_stdout", default_output = False, **kwargs)
    exception_on_error = libkw.handle_kwargs("exception_on_error", default_output = True, **kwargs)
    stop_on_exception = libkw.handle_kwargs("stop_on_exception", default_output = True, **kwargs)
    threads = []
    exceptions = []
    lock = threading.Lock()
    index = [0]
    stop_control = libstopcontrol.StopControl(mp.RLock())
    args_list = [lock, index, processes, process_filter, print_stderr, print_stdout, exception_on_error, stop_on_exception, log, exceptions, stop_control]
    for process in processes:
        stop_control.add(process)
    communications = []
    for i in range(jobs_count):
        parent_conn, child_conn = mp.Pipe()
        communications.append((parent_conn, child_conn))
        thread_name = f"scheduled job {i}"
        args_list_copy = args_list.copy()
        args_list_copy.append(thread_name)
        args_list_copy.append(child_conn)
        threads.append(mp.Process(target = target, args = args_list_copy))
    for thread in threads:
        thread.start()
    _executor = concurrent.ThreadPoolExecutor(max_workers = len(processes))
    futures = []
    for index, thread in enumerate(threads):
        futures.append(_executor.submit(handle_recv, communications[index][0]))
    for future in futures:
        future.result()
    for thread in threads:
        thread.join()
    return exceptions

def schedule_jobs_cmds(cmds, jobs_count, process_filter = lambda process: process, **kwargs):
    from pylibcommons import  libprocess
    processes = []
    for cmd in cmds:
        processes.append(libprocess.Process(cmd))
    return schedule_jobs(processes, jobs_count, process_filter = process_filter, **kwargs)
