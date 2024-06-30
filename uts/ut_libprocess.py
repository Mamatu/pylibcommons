__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from pylibcommons import libprocess

import logging
log = logging.getLogger(__name__)

import pytest
import pathlib
import os

def test_process_with_exception():
    uts_path = pathlib.Path(__file__).parent.resolve()
    path = os.path.join(uts_path, "data/ut_libprocess/data_no_existed.txt")
    process = libprocess.Process(f"grep 'text' {path}", exception_on_error=True)
    process.start()
    with pytest.raises(Exception):
        process.wait()
