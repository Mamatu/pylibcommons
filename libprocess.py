import psutil
import subprocess
import tempfile
import telnetlib
import time

import logging
log = logging.getLogger("pytorprivoxy")

from pylibcommons import libprint

class Process:
    log = log.getChild(__name__)
    def __init__(self, cmd):
        self.is_destroyed_flag = False
        import threading
        self.lock = threading.Lock()
        self.cmd = cmd
        self.process = None
    def was_stopped(self):
        return self.is_destroyed_flag
    def emit_warning_during_destroy(self, ex):
        log.warning(f"{ex}: please verify if process {self.cmd} was properly closed")
    def start(self):
        self.process = subprocess.Popen(self.cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True)
        log.info(f"Start process {self.process}")
    def stop(self):
        self.is_destroyed_flag = True
        if not hasattr(self, "process"):
            return
        if self.process is None:
            return
        self.process.stdout.close()
        self.process.stderr.close()
        try:
            import libterminate
            libterminate.terminate_process_and_children(self.process)
            self.process = None
        except psutil.NoSuchProcess as nsp:
            self.emit_warning_during_destroy(nsp)
        except subprocess.TimeoutExpired as te: 
            self.emit_warning_during_destroy(te)
        log.info(f"Stop process {self.process}")
    def wait(self):
        if self.process:
            self.process.wait()

def make(cmd):
    return Process(cmd)
