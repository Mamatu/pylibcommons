import psutil
import subprocess

from pylibcommons import libprint
from pylibcommons import libkw
from pylibcommons.private import libtemp

import logging
logging.basicConfig()
log = logging.getLogger(__name__)

class Process:
    class ReturnCodeException(Exception):
        def __init__(self, cmd, returncode):
            self.cmd = cmd
            self.returncode = returncode
            Exception.__init__(self, f"Return code is not zero in process {cmd}. It is {returncode}")
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
        if self.process:
            raise Exception(f"Process {self.cmd} already started {self.process}")
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
        libprint.print_func_info(logger = log.debug, extra_string = f"Cmd {self.cmd} files stdout: {self.get_fout_name()}, stderr: {self.get_ferr_name()}")
        process = subprocess.Popen(self.cmd, stdout = self.fout, stderr = self.ferr, universal_newlines = True, shell = self.shell)
        return process
    def get_fout_name(self):
        if self.fout is None:
            return None
        return self.fout.name
    def get_ferr_name(self):
        if self.ferr is None:
            return None
        return self.ferr.name
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
        libprint.print_func_info(logger = log.debug, extra_string = f"Stop process {self.process}")
        self.is_destroyed_flag = True
        if not hasattr(self, "process"):
            return
        if self.process is None:
            return
        self.cleanup()
    def cleanup(self):
        libprint.print_func_info(logger = log.debug, extra_string = f"Cleanup process {self.process}")
        try:
            import libterminate
            libterminate.terminate_process_and_children(self.process)
            self.process = None
        except psutil.NoSuchProcess as nsp:
            self.emit_warning_during_destroy(nsp)
        except subprocess.TimeoutExpired as te: 
            self.emit_warning_during_destroy(te)
    def get_returncode(self):
        if self.process is None:
            raise Exception(f"Process {self.cmd} not started")
        return self.process.returncode
    def wait(self, **kwargs):
        if not self.process:
            raise Exception("Process is not started")
        libprint.print_func_info(logger = log.debug, print_current_time = True)
        exception_on_error = libkw.handle_kwargs("exception_on_error", default_output = False, **kwargs)
        print_stdout = libkw.handle_kwargs("print_stdout", default_output = False, **kwargs)
        print_stderr = libkw.handle_kwargs("print_stderr", default_output = False, **kwargs)
        check_error_timeout = libkw.handle_kwargs("check_error_timeout", default_output = None, **kwargs)
        if isinstance(check_error_timeout, int) and check_error_timeout == 0:
            check_error_timeout = None
        def handle_stream(self, print_it, is_stream, get_stream, logger):
            if not print_it:
                return
            if is_stream():
                _std = get_stream()
                _std.seek(0)
                lines = _std.readlines()
                if len(lines) > 0:
                    lines = "".join(lines)
                    logger(lines)
        def handle_stderr(self):
            nonlocal print_stderr
            handle_stream(self, print_stderr, self.is_stderr, self.get_stderr, log.info)
        def handle_stdout(self):
            nonlocal print_stdout
            handle_stream(self, print_stdout, self.is_stdout, self.get_stdout, log.error)
        try:
            def handle_stds(self):
                handle_stderr(self)
                handle_stdout(self)
            returncode = None
            while returncode == None:
                try:
                    returncode = self.process.wait(timeout = check_error_timeout)
                except subprocess.TimeoutExpired:
                    pass
                handle_stds(self)
            if exception_on_error and returncode != 0:
                raise Process.ReturnCodeException(self.cmd, returncode)
        finally:
            libprint.print_func_info(logger = log.debug, print_current_time = True)

def make(cmd, delete_log_file = True):
    return Process(cmd, delete_log_file = delete_log_file)
