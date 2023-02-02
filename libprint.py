__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import copy
import inspect
from pylibcommons import libkw

def print_func_info(**kwargs):
    print(get_func_info(level = 2, **kwargs))

def print_func_info_in_methods(**kwargs):
    outer_kwargs = kwargs
    def _print_info(func):
        def wrapper(*args, **kwargs):
            inner_kwargs = parse_kwargs(kwargs, func)
            begin_end = libkw.handle_kwargs("begin_end", default_output = True, **inner_kwargs)
            prefix = None
            if begin_end:
                prefix = "+ "
            print_func_info(**inner_kwargs, prefix = prefix)
            try:
                return func(*args, **kwargs)
            finally:
                if begin_end:
                    print_func_info(**inner_kwargs, prefix = "- ")
        return wrapper
    def parse_kwargs(_kwargs, method):
        inner_kwargs = _kwargs.copy()
        function_name = libkw.handle_kwargs("function_name", default_output = None, **inner_kwargs)
        file_name = libkw.handle_kwargs(["file_name", "filename"], default_output = None, **inner_kwargs)
        lineno = libkw.handle_kwargs("lineno", default_output = None, **inner_kwargs)
        if function_name == None:
            inner_kwargs["function_name"] = method.__name__
        filename_lineno = get_filename_lineno(level = 3)
        if file_name == None:
            inner_kwargs["file_name"] = filename_lineno[0]
        if lineno == None:
            inner_kwargs["lineno"] = filename_lineno[1]
        return inner_kwargs
    def class_wrapper(clazz):
        methods = [method for method in dir(clazz) if not method.startswith("__")]
        for method in methods:
            orig_method = clazz.__dict__[method]
            def make_wrapper(orig_method):
                orig_method = orig_method
                @_print_info
                def wrapper(self, *args, **kwargs):
                    return orig_method(self, *args, **kwargs)
                return wrapper
            setattr(clazz, str(method), make_wrapper(orig_method))
        orig_init = clazz.__init__
        @_print_info
        def __init__(self, *args, **kwargs):
            return orig_init(self, *args, **kwargs)
        clazz.__init__ = __init__
        return clazz
    return class_wrapper

def get_caller_args(caller):
    args, varargs, keywords, values = inspect.getargvalues(caller)
    output = [(i, values[i]) for i in args]
    if varargs: output.extend([(i) for i in values[varargs]])
    if keywords: output.extend([(k, v) for k, v in values[keywords].items()])
    return output

def get_filename_lineno(level = 1):
    frame = inspect.stack()[level]
    class Wrapper:
        def __init__(self, frame):
            self.info = [frame.filename, frame.lineno]
        def __getitem__(self, i):
            return self.info[i]
        def set_filename(self, filename):
            self.info[0] = filename
        def set_lineno(self, lineno):
            self.info[1] = lineno
        def __len__(self):
            return len(self.info)
        def __str__(self):
            return f"{self.info[0]}:{self.info[1]}"
    return Wrapper(frame)

def get_caller_from_frame_or_level(frame_level):
    if isinstance(frame_level, int):
        frame_level = inspect.stack()[frame_level]
    return frame_level[0]

def get_func_info(level = 1, **kwargs):
    pfaloc = libkw.handle_kwargs("print_filename_and_linenumber_of_call", default_output = True, **kwargs)
    extra_string = libkw.handle_kwargs("extra_string", default_output = None, **kwargs)
    self_in_args_list = libkw.handle_kwargs("self_in_args_list", default_output = False, **kwargs)
    function_name = libkw.handle_kwargs("function_name", default_output = None, **kwargs)
    file_name = libkw.handle_kwargs(["file_name", "filename"], default_output = None, **kwargs)
    lineno = libkw.handle_kwargs("lineno", default_output = None, **kwargs)
    prefix = libkw.handle_kwargs("prefix", default_output = None, **kwargs)
    frame = inspect.stack()[level]
    caller = get_caller_from_frame_or_level(frame)
    if function_name == None:
        function_name = frame[3]
    filename_lineno = get_filename_lineno(level = level)
    if file_name != None:
        filename_lineno.set_filename(file_name)
    if lineno != None:
        filename_lineno.set_lineno(lineno)
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
    output = f"{function_name} ({args})"
    if prefix:
        output = f"{prefix}{output}"
    if pfaloc:
        output = f"{output} {filename_lineno}"
    if extra_string:
        output = f"{output} {extra_string}"
    return output
