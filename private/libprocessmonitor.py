from pylibcommons import libthread

class ProcessMonitor(libthread.Thread):
    def __init__(self, process, callback):
        self.process = process
        self.callback = callback
        def target(process, callback, stop_control):
            def read_stream(has_stream, get_stream):
                if has_stream():
                    _std = get_stream()
                    _std.seek(0)
                    lines = _std.readlines()
                    return lines
                return []
            while not stop_control.is_stopped():
                lines = read_stream(process.has_stdout, process.get_stdout)
                if len(lines) > 0:
                    callback("stdout", lines)
                lines = read_stream(process.has_stderr, process.get_stderr)
                if len(lines) > 0:
                    callback("stderr", lines)
                returncode = process.poll()
                if returncode is not None:
                    callback("returncode", returncode)
                    stop_control.stop()
                stop_control.wait_for_stop(timeout = 1.)
        super().__init__(target, args = [self.process, self.callback], thread_name = f"Process monitor for {self.process}")
