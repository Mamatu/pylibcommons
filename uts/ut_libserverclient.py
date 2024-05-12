__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from pylibcommons import libprint, libserver
from multiprocessing.connection import Client

from time import sleep

import logging
log = logging.getLogger(__name__)

def test_connection(mocker):
    libprint.print_func_info(prefix = "+", logger = log.debug)
    def _handler(line, client):
        assert line == "test"
        libprint.print_func_info(prefix = "+", logger = log.debug)
        return libserver.StopExecution()
    handler = mocker.Mock()
    handler.side_effect = _handler
    server = libserver.run(handler, ("localhost", 7000))
    client = Client(("localhost", 7000))
    client.send("test")
    sleep(1)
    server.stop()
    server.wait_for_finish()
    handler.assert_called_once()
    libprint.print_func_info(prefix = "-", logger = log.debug)
