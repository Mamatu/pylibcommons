__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from unittest import mock
import pytest

@mock.patch("time.sleep")
@mock.patch("time.time")
def test_while_with_timeout(time_time_mock, time_sleep_mock):
    from pylibcommons import libloop
    with pytest.raises(libloop.TimeoutException) as excinfo:
        time_sleep_mock.side_effect = lambda x: print(f"Sleeping for {x} seconds")
        time_time_mock.side_effect = [0, 0, 0.7, 1] 
        def condition():
            return True
        libloop.while_with_timeout(timeout = 1, condition = condition, time_sleep = 0.7)
    time_sleep_mock.assert_has_calls([mock.call(0.7), mock.call(1 - 0.7)])

@mock.patch("time.sleep")
@mock.patch("time.time")
def test_while_with_timeout_1(time_time_mock, time_sleep_mock):
    from pylibcommons import libloop
    time_sleep_mock.side_effect = lambda x: print(f"Sleeping for {x} seconds")
    time_time_mock.side_effect = [0, 0, 0.7, 1] 
    def condition():
        return False, 123
    assert 123 == libloop.while_with_timeout(timeout = 1, condition = condition, time_sleep = 0.7)
