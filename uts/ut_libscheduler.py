__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"


import logging
log = logging.getLogger(__name__)

from pylibcommons.libscheduler import schedule_jobs

def test_schedule_jobs_1():
    class Process:
        def __init__(self):
            self.is_started = False
            self.is_waited = False
        def start(self):
            self.is_started = True
        def wait(self, **kwargs):
            self.is_waited = True
    processes = [Process()]
    schedule_jobs(processes, 1)
    assert processes[0].is_started
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
