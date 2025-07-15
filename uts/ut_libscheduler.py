__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import logging
log = logging.getLogger(__name__)

from pylibcommons.libscheduler import schedule_jobs, schedule_jobs_multiprocesses
import threading

from multiprocessing import Value
import sys

def test_schedule_mp_1():
    class Process:
        def __init__(self):
            self._counter = Value('i', 0)
            self._is_started = Value('b', False)
            self._is_stopped = Value('b', False)
            self._is_waited = Value('b', False)
        def start(self):
            while not self._is_stopped.value:
                self._counter.value += 1
                if self._counter.value == 5:
                    self._is_stopped.value = True
                    break
        def wait(self, **kwargs):
            self._is_waited.value = True
        def stop(self):
            self._is_stopped.value = True
        def wait_for_stop(self, timeout = None):
            pass
        def is_stopped(self):
            return self._is_stopped.value
    #process = create_process_for(schedule_jobs_multiprocesses, Process())
    processes = [Process()]
    schedule_jobs_multiprocesses(processes, 1)
    print(processes[0]._counter.__dict__)
    assert processes[0]._is_started
    assert processes[0]._is_waited
    assert processes[0]._counter.value == 5

def test_schedule_mp_2():
    class Process:
        def __init__(self):
            self._counter = Value('i', 0)
            self._is_started = Value('b', False)
            self._is_stopped = Value('b', False)
            self._is_waited = Value('b', False)
        def start(self):
            while not self._is_stopped.value:
                self._counter.value += 1
                if self._counter.value == 5:
                    self._is_stopped.value = True
                    break
        def wait(self, **kwargs):
            self._is_waited.value = True
        def stop(self):
            self._is_stopped.value = True
        def wait_for_stop(self, timeout = None):
            pass
        def is_stopped(self):
            return self._is_stopped.value
    #process = create_process_for(schedule_jobs_multiprocesses, Process())
    processes = [Process(), Process()]
    schedule_jobs_multiprocesses(processes, 1)
    print(processes[0]._counter.__dict__)
    assert processes[0]._is_started
    assert processes[0]._is_waited
    assert processes[0]._counter.value == 5
    assert processes[1]._is_started
    assert processes[1]._is_waited
    assert processes[1]._counter.value == 5

def test_schedule_mp_3():
    class Process:
        def __init__(self, index):
            self.index = Value('i', index)
            self._counter = Value('i', 0)
            self._is_started = Value('b', False)
            self._is_stopped = Value('b', False)
            self._is_waited = Value('b', False)
        def start(self):
            while not self._is_stopped.value:
                self._counter.value += 1
                if self._counter.value == self.index.value * 5:
                    self._is_stopped.value = True
                    break
        def wait(self, **kwargs):
            self._is_waited.value = True
        def stop(self):
            self._is_stopped.value = True
        def wait_for_stop(self, timeout = None):
            pass
        def is_stopped(self):
            return self._is_stopped.value
    processes = [Process(1), Process(2), Process(3), Process(4)]
    schedule_jobs_multiprocesses(processes, 2)
    for index in range(4):
        assert processes[index]._is_started
        assert processes[index]._is_waited
        assert processes[index]._counter.value == (index + 1) * 5

def test_schedule_jobs_1():
    class Process:
        def __init__(self):
            self.is_started = False
            self.is_waited = False
            self.lock = threading.Lock()
        def start(self):
            with self.lock:
                self.is_started = True
        def wait(self, **kwargs):
            self.is_waited = True
        def stop(self):
            pass
        def wait_for_stop(self, timeout = None):
            pass
        def is_stopped(self):
            return False
    processes = [Process()]
    schedule_jobs(processes, 1)
    assert processes[0].is_waited

def test_schedule_jobs_2():
    class Process:
        def __init__(self):
            self.is_started = False
            self.is_waited = False
        def start(self):
            self.is_started = True
        def wait(self, **kwargs):
            self.is_waited = True
    processes = [Process(), Process()]
    schedule_jobs(processes, 1)
    assert processes[0].is_started
    assert processes[0].is_waited
    assert processes[1].is_started
    assert processes[1].is_waited

def test_schedule_jobs_3():
    class Process:
        def __init__(self):
            self.is_started = False
            self.is_waited = False
        def start(self):
            self.is_started = True
        def wait(self, **kwargs):
            self.is_waited = True
    processes = []
    processes.append(Process())
    processes.append(Process())
    processes.append(Process())
    processes.append(Process())
    processes.append(Process())
    processes.append(Process())
    schedule_jobs(processes, 2)
    assert processes[0].is_started
    assert processes[0].is_waited
    assert processes[1].is_started
    assert processes[1].is_waited
    assert processes[2].is_started
    assert processes[2].is_waited
    assert processes[3].is_started
    assert processes[3].is_waited
    assert processes[4].is_started
    assert processes[4].is_waited
    assert processes[5].is_started
    assert processes[5].is_waited

def test_schedule_jobs_4():
    class Process:
        def __init__(self):
            self.is_started = False
            self.is_waited = False
        def start(self):
            self.is_started = True
        def wait(self, **kwargs):
            self.is_waited = True
    processes = []
    processes.append(Process())
    processes.append(Process())
    processes.append(Process())
    schedule_jobs(processes, 6)
    assert processes[0].is_started
    assert processes[0].is_waited
    assert processes[1].is_started
    assert processes[1].is_waited
    assert processes[2].is_started
    assert processes[2].is_waited

def test_schedule_jobs_stop_on_exception_2_jobs():
    class Process:
        def __init__(self):
            self.is_started = False
            self.is_waited = False
            self.is_stopped = False
            self.processes = None
        def start(self):
            self.is_started = True
            if self.processes is None:
                raise Exception("self.processes is None")
            if all([p.is_started for p in self.processes]):
                raise Exception("Test exception")
        def stop(self):
            self.is_stopped = True
        def wait(self, **kwargs):
            self.is_waited = True
    processes = []
    processes.append(Process())
    processes.append(Process())
    processes[0].processes = processes
    processes[1].processes = processes
    schedule_jobs(processes, 2)
    assert processes[0].is_started
    assert processes[1].is_started

def test_schedule_jobs_stop_on_exception_4_jobs():
    class Process:
        def __init__(self):
            self.is_started = False
            self.is_waited = False
            self.is_stopped = False
            self.processes = None
        def start(self):
            self.is_started = True
            if self.processes is None:
                raise Exception("self.processes is None")
            if all([p.is_started for p in self.processes]):
                raise Exception("Test exception")
        def stop(self):
            self.is_stopped = True
        def wait(self, **kwargs):
            self.is_waited = True
    processes = []
    processes.append(Process())
    processes.append(Process())
    processes[0].processes = processes
    processes[1].processes = processes
    schedule_jobs(processes, 4)
    assert processes[0].is_started
    assert processes[1].is_started
