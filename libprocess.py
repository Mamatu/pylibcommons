import psutil
import subprocess
import tempfile
import time

import logging
log = logging.getLogger(__name__)

import libprint

from pylibcommons import libprint
from pylibcommons.private import libtemp

class Process:
    log = log.getChild(__name__)
    def __init__(self, cmd, use_temp_file = True, shell = True, timeout = None, delete_log_file = True):
        self.is_destroyed_flag = False
        self.cmd = cmd
        self.process = None
        self.use_temp_file = use_temp_file
        self.delete_log_file = delete_log_file
        if self.use_temp_file is False and self.delete_log_file is False:
            raise ValueError("delete_log_file can be True if use_temp_file is True")
        self.shell = shell
        self.fout = None
        self.ferr = None
        self.timeout = timeout
    def was_stopped(self):
        return self.is_destroyed_flag
    def emit_warning_during_destroy(self, ex):
        libprint.print_func_info(logger = log.warn, extra_string = f"{ex}: please verify if process {self.cmd} was properly closed")
    def start(self):
        self.process = None
        if self.use_temp_file:
            self.process = self._start_temp_files()
        else:
            self.process = self._start_pipes()
        libprint.print_func_info(logger = log.debug, extra_string = f"Start process {self.process}")
    def _start_pipes(self):
        return subprocess.Popen(self.cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True, shell = self.shell)
    def _start_temp_files(self):
        self.fout = libtemp.create_temp_file(delete = self.delete_log_file)
        self.ferr = libtemp.create_temp_file(delete = self.delete_log_file)
        libprint.print_func_info(logger = log.info, extra_string = f"Cmd {self.cmd} files stdout: {self.fout.name}, stderr: {self.ferr.name}")
        process = subprocess.Popen(self.cmd, stdout = self.fout, stderr = self.ferr, universal_newlines = True, shell = self.shell)
        return process
    def is_stderr(self):
        if self.ferr is not None:
            return True
        return hasattr(self.process, "stderr")
    def is_stdout(self):
        if self.fout is not None:
            return True
        return hasattr(self.process, "stdout")
    def get_stderr(self):
        if self.ferr:
            self.ferr.seek(0)
            return self.ferr
        if self.process is None:
            return None
        return self.process.stderr
    def get_stdout(self):
        if self.fout:
            self.fout.seek(0)
            return self.fout
        if self.process is None:
            return None
        return self.process.stdout
    def stop(self):
        self.is_destroyed_flag = True
        if not hasattr(self, "process"):
            return
        if self.process is None:
            return
        if self.process.stdout:
            self.process.stdout.close()
        if self.process.stderr:
            self.process.stderr.close()
        try:
            import libterminate
            libterminate.terminate_process_and_children(self.process)
            self.process = None
        except psutil.NoSuchProcess as nsp:
            self.emit_warning_during_destroy(nsp)
        except subprocess.TimeoutExpired as te: 
            self.emit_warning_during_destroy(te)
        libprint.print_func_info(logger = log.debug, extra_string = f"Stop process {self.process}")
    def wait(self):
        if self.process:
            self.process.wait()

def make(cmd, delete_log_file = True):
    return Process(cmd, delete_log_file = delete_log_file)
