from multiprocessing.connection import Client
from pylibcommons import libprint
import logging

log = logging.getLogger(__name__)

def create(port):
    libprint.print_func_info(prefix = "+", logger = log.debug)
    try:
        address = ("localhost", port)
        return _Client(address)
    finally:
        libprint.print_func_info(prefix = "-", logger = log.debug)

class _Client:
    def __init__(self, address):
        self.conn = Client(address)
    def write(self, msg):
        self.conn.send(msg)
    def __del__(self):
        self.conn.close()

