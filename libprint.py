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
    level = libkw.handle_kwargs("level", default_output = 1, **kwargs)
    kwargs["level"] = level + 1
    print(get_func_info(**kwargs))

def class_debug_prints(**kwargs):
    outer_kwargs = kwargs
    def _print_info(orig_method):
        def wrapper_func(func):
            def wrapper(self, *args, **kwargs):
                inner_kwargs = outer_kwargs.copy()
                begin_end = libkw.handle_kwargs("begin_end", default_output = True, **inner_kwargs)
                prefix = None
                if begin_end:
                    prefix = "+ "
                filename_lineno = get_filename_lineno(level = 2)
                inner_kwargs["filename"] = filename_lineno[0]
                inner_kwargs["lineno"] = filename_lineno[1]
                inner_kwargs["function_name"] = orig_method.__name__
                inner_kwargs["args"] = convert_args_to_str(level = 1)
                print_func_info(**inner_kwargs, prefix = prefix)
                try:
                    return func(self, *args, **kwargs)
                finally:
                    if begin_end:
                        print_func_info(**inner_kwargs, prefix = "- ")
            return wrapper
        return wrapper_func
    def class_wrapper(clazz):
        predicate = lambda x: inspect.ismethod(x) or inspect.isfunction(x)
        methods = inspect.getmembers(clazz, predicate = predicate)
        methods = [method[0] for method in methods if not method[0].startswith("__")]
        for method in methods:
            orig_method = clazz.__dict__[method]
            def make_wrapper(orig_method):
                orig_method = orig_method
                @_print_info(orig_method)
                def wrapper(self, *args, **kwargs):
                    return orig_method(self, *args, **kwargs)
                return wrapper
            setattr(clazz, str(method), make_wrapper(orig_method))
        orig_init = clazz.__init__
        @_print_info(orig_init)
        def __init__(self, *args, **kwargs):
            return orig_init(self = self, *args, **kwargs)
        clazz.__init__ = __init__
        return clazz
    return class_wrapper

def get_caller_args(caller):
    args, varargs, keywords, values = inspect.getargvalues(caller)
    output = [(i, values[i]) for i in args]
    if varargs: output.extend([(i) for i in values[varargs]])
    if keywords: output.extend([(k, v) for k, v in values[keywords].items()])
    return output

class Filename_Lineno:
    def __init__(self, filename, lineno):
        self.info = [filename, lineno]
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
    def is_valid(self):
        return self.info[0] and self.info[1]
    @staticmethod
    def from_frame(frame):
        return Filename_Lineno(frame.filename, frame.lineno)
    @staticmethod
    def empty():
        return Filename_Lineno(None, None)

def get_filename_lineno(**kwargs):
    level = libkw.handle_kwargs("level", default_output = None, **kwargs)
    file_name = libkw.handle_kwargs(["file_name", "filename"], default_output = None, **kwargs)
    lineno = libkw.handle_kwargs("lineno", default_output = None, **kwargs)
    filename_lineno = Filename_Lineno.empty()
    if level is not None:
        frame = inspect.stack()[level]
        filename_lineno = Filename_Lineno.from_frame(frame)
    if file_name is not None:
        filename_lineno.set_filename(file_name)
    if lineno is not None:
        filename_lineno.set_lineno(lineno)
    return filename_lineno

def get_function_name(level = 1):
    frame = inspect.stack()[level]
    return frame[3]

def get_caller_from_frame_or_level(frame_level):
    if isinstance(frame_level, int):
        frame_level = inspect.stack()[frame_level]
    return frame_level[0]

def get_func_args(**kwargs):
    level = libkw.handle_kwargs("level", default_output = 1, **kwargs)
    frame = inspect.stack()[level]
    caller = get_caller_from_frame_or_level(frame)
    return get_caller_args(caller)

def convert_args_to_str(**kwargs):
    level = libkw.handle_kwargs("level", default_output = 1, **kwargs)
    args = libkw.handle_kwargs("args", default_output = None, **kwargs)
    if args is None:
        args = get_func_args(level = level + 1)
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
    return args.replace("[", "").replace("]", "").replace("\"", "")
    
def get_func_info(**kwargs):
    level = libkw.handle_kwargs("level", default_output = 1, **kwargs)
    pfaloc = libkw.handle_kwargs("print_filename_and_linenumber_of_call", default_output = True, **kwargs)
    extra_string = libkw.handle_kwargs("extra_string", default_output = None, **kwargs)
    function_name = libkw.handle_kwargs("function_name", default_output = None, **kwargs)
    file_name = libkw.handle_kwargs(["file_name", "filename"], default_output = None, **kwargs)
    lineno = libkw.handle_kwargs("lineno", default_output = None, **kwargs)
    prefix = libkw.handle_kwargs("prefix", default_output = None, **kwargs)
    args = libkw.handle_kwargs("args", default_output = None, **kwargs)
    if args is None:
        args = convert_args_to_str(level = level + 1)
    if function_name is None:
        function_name = get_function_name(level = level + 1)
    output = f"{function_name} ({args})"
    filename_lineno = get_filename_lineno(level = level + 1)
    if file_name is not None:
        filename_lineno.set_filename(file_name)
    if lineno is not None:
        filename_lineno.set_lineno(lineno)
    if prefix:
        output = f"{prefix}{output}"
    if pfaloc:
        output = f"{output} {filename_lineno}"
    if extra_string:
        output = f"{output} {extra_string}"
    return output
