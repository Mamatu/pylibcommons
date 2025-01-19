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
                wait_kwargs = {"print_stderr": print_stderr, "print_stdout" : print_stdout, "exception_on_error" : exception_on_error}
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

def schedule_jobs_cmds(cmds, jobs_count, process_filter = lambda process: process, **kwargs):
    from pylibcommons import  libprocess
    processes = []
    for cmd in cmds:
        processes.append(libprocess.Process(cmd))
    return schedule_jobs(processes, jobs_count, process_filter = process_filter, **kwargs)
