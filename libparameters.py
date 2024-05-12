__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import inspect

def verify_parameters(func, expected_args):
    def get_args(func):
        args = inspect.getfullargspec(func)
        args = args.args
        if hasattr(func, "__self__"):
            args.pop(0)
        return args
    if isinstance(expected_args, str):
        expected_args = [expected_args]
    full_spec_args = get_args(func)
    if len(expected_args) != len(full_spec_args):
        raise Exception(f"Function {func} doesn't have expected args {expected_args}. It has {full_spec_args}")
    for arg_name in expected_args:
        if arg_name not in full_spec_args:
            raise Exception(f"Function {func} must have {arg_name} parameter")
