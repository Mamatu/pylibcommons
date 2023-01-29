__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import inspect

def get_caller_args(caller):
    args, varargs, keywords, values = inspect.getargvalues(caller)
    output = [(i, values[i]) for i in args]
    if varargs: output.extend([(i) for i in values[varargs]])
    if keywords: output.extend([(k, v) for k, v in values[keywords].items()])
    return output

def get_func_info(level = 1, print_filename_and_linenumber_of_call = True):
    frame = inspect.stack()[level]
    caller = frame[0]
    function_name = frame[3]
    args = get_caller_args(caller)
    for arg in args:
        if isinstance(arg, tuple):
            if len(arg) == 2:
                idx = args.index(arg)
                if isinstance(arg[1], str):
                    args[idx] = f"{arg[0]} = \'{arg[1]}\'"
                else:
                    args[idx] = f"{arg[0]} = {arg[1]}"
            elif len(arg) == 1:
                args[idx] = f"{arg[0]}"
            else:
                raise Exception("Not supported length of arg")
    args = map(lambda arg: str(arg), args)
    args = ", ".join(args)
    args = args.replace("[", "").replace("]", "").replace("\"", "")
    if print_filename_and_linenumber_of_call:
        return f"{function_name} ({args}) {frame.filename}:{frame.lineno}"
    return f"{function_name} ({args})"

def print_func_info(print_filename_and_linenumber_of_call = True):
    print(get_func_info(level = 2, print_filename_and_linenumber_of_call = print_filename_and_linenumber_of_call))
