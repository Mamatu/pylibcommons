__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import inspect
from pylibcommons import libkw

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

def get_func_info(level = 1, **kwargs):
    pfaloc = libkw.handle_kwargs("print_filename_and_linenumber_of_call", default_output = True, **kwargs)
    extra_string = libkw.handle_kwargs("extra_string", default_output = None, **kwargs)
    self_in_args_list = libkw.handle_kwargs("self_in_args_list", default_output = False, **kwargs)
    function_name = libkw.handle_kwargs("function_name", default_output = None, **kwargs)
    file_name = libkw.handle_kwargs(["file_name", "filename"], default_output = None, **kwargs)
    lineno = libkw.handle_kwargs("lineno", default_output = None, **kwargs)
    frame = inspect.stack()[level]
    caller = frame[0]
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
    if pfaloc:
        output = f"{output} {filename_lineno}"
    if extra_string:
        output = f"{output} {extra_string}"
    return output

def print_func_info(**kwargs):
    print(get_func_info(level = 2, **kwargs))

def print_func_info_in_methods(**kwargs):
    outer_kwargs = kwargs
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
            def wrapper(self, *args, **kwargs):
                inner_kwargs = parse_kwargs(outer_kwargs, orig_method)
                print_func_info(**inner_kwargs)
                return orig_method(self, *args, **kwargs)
            setattr(clazz, str(method), wrapper)
        orig_init = clazz.__init__
        def __init__(self, *args, **kwargs):
            inner_kwargs = parse_kwargs(outer_kwargs, orig_init)
            print_func_info(**inner_kwargs)
            orig_init(self, *args, **kwargs)
        clazz.__init__ = __init__
        return clazz
    return class_wrapper
