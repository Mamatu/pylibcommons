from pylibcommons import libprint
import logging

log = logging.getLogger(__name__)

def send(msg, port):
    libprint.print_func_info(prefix = "+", logger = log.debug)
    from multiprocessing.connection import Client
    address = ("localhost", port)
    conn = Client(address)
    try:
        conn.send(msg)
    finally:
        conn.close()
        libprint.print_func_info(prefix = "-", logger = log.debug)
