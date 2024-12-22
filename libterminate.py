__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

def terminate_process_and_children(process):
    if process is None:
        return
    import subprocess
    import psutil
    parent = psutil.Process(process.pid)
    children = parent.children(recursive=True)
    for child in children:
        child.terminate()
    process.terminate()
    try:
        process.wait(timeout = 1)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout = 1)
    if process and hasattr(process, "stdout") and process.stdout:
        process.stdout.close()
    if process and hasattr(process, "stderr") and process.stderr:
        process.stderr.close()
