__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import datetime
import logging
import os

from pylibcommons import libprint, libgrep, libserver, libclient

import pytest
import re

log = logging.getLogger(__name__)

def test_connection(mocker):
    libprint.print_func_info(prefix = "+", logger = log.debug)
    def _handler(line):
        assert line == "test"
        libprint.print_func_info(prefix = "+", logger = log.debug)
        return libserver.StopExecution()
    handler = mocker.Mock()
    handler.side_effect = _handler
    def server_before_accept():
        libprint.print_func_info(prefix = "+", logger = log.debug)
        client = libclient.create(7000)
        client.write("test")
        libprint.print_func_info(prefix = "-", logger = log.debug)
    server = libserver.run(handler, 7000, server_before_accept = server_before_accept)
    server.wait_for_finish()
    handler.assert_called_once()
    libprint.print_func_info(prefix = "-", logger = log.debug)
