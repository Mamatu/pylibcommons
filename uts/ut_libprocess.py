__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

def test_process_with_exception():
    import logging
    log = logging.getLogger(__name__)
    from pylibcommons import libprocess
    import pytest
    import pathlib
    import os
    uts_path = pathlib.Path(__file__).parent.resolve()
    path = os.path.join(uts_path, "data/ut_libprocess/data_no_existed.txt")
    process = libprocess.Process(f"grep 'text' {path}")
    process.start()
    with pytest.raises(Exception):
        process.wait(exception_on_error=True)

def test_process_with_returncode_1(capsys):
    import logging
    log = logging.getLogger(__name__)
    import pytest
    import pathlib
    import os
    from pylibcommons import libprocess
    from sys import stderr
    from sys import stdout
    def make_list(stream):
        out = stream
        out = out.split("\n")
        out.remove('')
        return out
    uts_path = pathlib.Path(__file__).parent.resolve()
    path = os.path.join(uts_path, "data/ut_libprocess/script1.py")
    process = libprocess.Process(f"PYTHONPATH=.. python3 {path}")
    process.start()
    with pytest.raises(libprocess.Process.ReturnCodeException) as excinfo:
        process.wait(exception_on_error = True)
    assert excinfo.value.returncode == 1
