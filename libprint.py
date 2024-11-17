__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import inspect
from pylibcommons import libkw

import datetime

def print_func_info(**kwargs):
    level = libkw.handle_kwargs("level", default_output = 1, **kwargs)
    logger = libkw.handle_kwargs("logger", default_output = print, **kwargs)
    kwargs["level"] = level + 1
    logger(get_func_info(**kwargs))

_global_strings = []

def add_global_string(string):
    global _global_strings
    _global_strings.append(string)

def clear_global_string():
    global _global_strings
    _global_strings = []

def set_global_string(string):
    clear_global_string()
    add_global_string(string)

def get_global_strings():
    global _global_strings
    return _global_strings.copy()

def setup_logger(logger):
    import logging
    import sys
    def create_handler(sysstream, level, _filter):
        h = logging.StreamHandler(sysstream)
        h.setLevel(level)
        h.addFilter(_filter)
        return h
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    logger.addHandler(create_handler(sys.stdout, logging.DEBUG, lambda record: record.levelno <= logging.INFO))
    logger.addHandler(create_handler(sys.stderr, logging.WARN, lambda record: record.levelno > logging.INFO))

def func_info(logger = print):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print_func_info(prefix = "+", logger = logger, function_name = f"{func.__name__}@wrapper", print_filename = False, print_linenumber = False)
            try:
                return func(*args, **kwargs)
            finally:
                print_func_info(prefix = "-", logger = logger, function_name = f"{func.__name__}@wrapper", print_filename = False, print_linenumber = False)
        return wrapper
    return decorator

def class_debug_prints(**kwargs):
    """
    Not to use. It seems that there is no a way in python to handle properly this type of decorator
    """
    from warnings import warn
    warn("Not to use. It seems that there is no a way in python to handle properly this type of decorator")
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
                inner_kwargs["args"] = convert_args_to_str(level = 1, **kwargs, arg_length_limit = None)
                print_func_info(**inner_kwargs, prefix = prefix, arg_length_limit = None)
                try:
                    return func(self, *args, **kwargs)
                finally:
                    if begin_end:
                        print_func_info(**inner_kwargs, prefix = "- ", arg_length_limit = None)
            return wrapper
        return wrapper_func
    def class_wrapper(clazz):
        predicate = lambda x: inspect.ismethod(x) or inspect.isfunction(x)
        methods = inspect.getmembers(clazz, predicate = predicate)
        methods = [method[0] for method in methods if not method[0].startswith("_")]
        for method in methods:
            if method not in clazz.__dict__:
                continue
            orig_method = clazz.__dict__[method]
            def make_wrapper(orig_method):
                orig_method = orig_method
                @_print_info(orig_method)
                def wrapper(self, *args, **kwargs):
                    return orig_method(self, *args, **kwargs)
                return wrapper
            setattr(clazz, str(method), make_wrapper(orig_method))
        is_handle_init = libkw.handle_kwargs("handle_init", default_output = False, **outer_kwargs)
        if is_handle_init:
            orig_init = clazz.__init__
            @_print_info(orig_init)
            def __init__(self, *args, **kwargs):
                return orig_init(self = self, *args, **kwargs)
            clazz.__init__ = __init__
        return clazz
    return class_wrapper

def get_caller_args(caller):
    args, varargs, keywords, values = inspect.getargvalues(caller)
    output = [(_ArgName(i), values[i]) for i in args]
    if varargs: output.extend([(i) for i in values[varargs]])
    if keywords: output.extend([(_ArgName(k), v) for k, v in values[keywords].items()])
    return output

class Filename_Lineno:
    def __init__(self, filename, lineno):
        self.info = [filename, lineno]
        self.print_filename = True
        self.print_linenumber = True
    def __getitem__(self, i):
        return self.info[i]
    def set_filename(self, filename):
        self.info[0] = filename
    def set_lineno(self, lineno):
        self.info[1] = lineno
    def set_print_filename(self, enable):
        self.print_filename = enable
    def set_print_linenumber(self, enable):
        self.print_linenumber = enable
    def __len__(self):
        return len(self.info)
    def __str__(self):
        _str = ""
        if self.print_filename:
            _str = f"{self.info[0]}"
        if self.print_filename and self.print_linenumber:
            _str = f"{_str}:"
        if self.print_linenumber:
            _str = f"{_str}{self.info[1]}"
        return _str
    def is_printed(self):
        return self.print_filename or self.print_linenumber
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

def limit_length(arg, **kwargs):
    arg_length_limit = libkw.handle_kwargs("arg_length_limit", default_output = 100, **kwargs)
    if arg_length_limit is not None:
        if len(arg) > arg_length_limit:
            return f"{arg[:arg_length_limit]}..."
    return arg

def convert_args_to_str(**kwargs):
    level = libkw.handle_kwargs("level", default_output = 1, **kwargs)
    args = libkw.handle_kwargs("args", default_output = None, **kwargs)
    if args is None:
        args = get_func_args(level = level + 1)
    for arg in args:
        idx = args.index(arg)
        if isinstance(arg, list) or isinstance(arg, tuple):
            if len(arg) == 2:
                arg0 = f"{arg[0]}, "
                arg1 = limit_length(str(arg[1]), **kwargs)
                if type(arg[0]) == _ArgName:
                    arg0 = f"{arg[0]} = "
                if isinstance(arg[1], str):
                    arg = f"{arg0}\'{arg1}\'"
                elif isinstance(arg[1], list):
                    arg = f"{arg0}{arg1}"
                elif isinstance(arg[1], tuple):
                    arg = f"{arg0}{arg1}"
                else:
                    arg = f"{arg0}{arg1}"
            elif len(arg) == 1:
                arg = f"{limit_length(arg[0])}"
            elif len(arg) > 1:
                arg = limit_length(str(arg))
        args[idx] = arg
    args = map(lambda arg: str(arg), args)
    args = list(args)
    return ", ".join(args)

def get_func_info(**kwargs):
    level = libkw.handle_kwargs("level", default_output = 1, **kwargs)
    print_filename = libkw.handle_kwargs("print_filename", default_output = True, **kwargs)
    print_linenumber = libkw.handle_kwargs("print_linenumber", default_output = True, **kwargs)
    print_function = libkw.handle_kwargs("print_function", default_output = True, **kwargs)
    extra_string = libkw.handle_kwargs("extra_string", default_output = None, **kwargs)
    function_name = libkw.handle_kwargs("function_name", default_output = None, **kwargs)
    file_name = libkw.handle_kwargs(["file_name", "filename"], default_output = None, **kwargs)
    lineno = libkw.handle_kwargs("lineno", default_output = None, **kwargs)
    prefix = libkw.handle_kwargs("prefix", default_output = None, **kwargs)
    args = libkw.handle_kwargs("args", default_output = None, **kwargs)
    print_current_time = libkw.handle_kwargs("print_current_time", default_output = True, **kwargs)
    ct = ""
    if print_current_time:
        ct = datetime.datetime.now()
        ct = ct.strftime("%Y-%m-%d %H:%M:%S.%f")
        ct = f"{ct}"
    if args is None:
        kwargs_1 = kwargs.copy()
        kwargs_1["level"] = level + 1
        args = convert_args_to_str(**kwargs_1)
    if function_name is None:
        function_name = get_function_name(level = level + 1)
    output = f"{ct}"
    if print_function:
        if output:
            output = f"{output} "
        output = f"{output}{function_name} ({args})"
    filename_lineno = get_filename_lineno(level = level + 1)
    if file_name is not None:
        filename_lineno.set_filename(file_name)
    if lineno is not None:
        filename_lineno.set_lineno(lineno)
    if prefix:
        if output:
            output = f"{output} "
        output = f"{prefix}{output}"
    filename_lineno.set_print_filename(print_filename)
    filename_lineno.set_print_linenumber(print_linenumber)
    if filename_lineno.is_printed():
        if output:
            output = f"{output} "
        output = f"{output}{filename_lineno}"
    if extra_string:
        if output:
            output = f"{output} "
        output = f"{output}{extra_string}"
    gs = get_global_strings()
    if len(gs) > 0:
        output = f"{'|'.join(gs)} {output}"
    return output

class _ArgName:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return str(self) == str(other)
