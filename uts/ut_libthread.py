__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from pylibcommons import libthread, libstopcontrol

import logging
log = logging.getLogger(__name__)

def test_stop_async_1_threads():
    def target(is_stopped, stop_control):
        stop_control.wait_for_stop()
        is_stopped[0] = True
    is_stopped = [False]
    thread = libthread.Thread(target, args = [is_stopped])
    thread.start()
    stop_control = thread.get_stop_control()
    stop_control.stop()
    thread.join()
    assert is_stopped[0] == True

def test_stop_async_2_threads():
    def target(is_stopped, index, stop_control):
        stop_control.wait_for_stop()
        is_stopped[index] = True
    is_stopped = [False, False]
    stop_control = libstopcontrol.StopControl()
    threads = []
    threads.append(libthread.Thread(target, stop_control = stop_control, args = [is_stopped, 0]))
    threads.append(libthread.Thread(target, stop_control = stop_control, args = [is_stopped, 1]))
    for thread in threads: thread.start()
    stop_control = thread.get_stop_control()
    stop_control.stop()
    for thread in threads: thread.join()
    assert is_stopped[0] == True
    assert is_stopped[1] == True
