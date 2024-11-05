from pylibcommons import libthread

class ProcessMonitor(libthread.Thread):
    def __init__(self, process, callback, logger = None):
        self.process = process
        self.callback = callback
        self.logger = logger
        def target(self, process, callback, stop_control):
            while not stop_control.is_stopped():
                lines = self.read_stream(process.has_stdout, process.get_stdout, self.logger)
                if len(lines) > 0:
                    callback("stdout", lines)
                lines = self.read_stream(process.has_stderr, process.get_stderr, self.logger)
                if len(lines) > 0:
                    callback("stderr", lines)
                returncode = process.poll()
                if returncode is not None:
                    callback("returncode", returncode)
                    stop_control.stop()
                stop_control.wait_for_stop(timeout = 1.)
        super().__init__(target, args = [self, self.process, self.callback], thread_name = f"Process monitor for {self.process}")
    def read_stream(self, has_stream, get_stream, logger):
        if has_stream():
            _std = get_stream()
            _std.seek(0)
            lines = _std.readlines()
            if len(lines) > 0:
                lines = "".join(lines)
                if logger:
                    logger(lines)
                return lines
        return ""
