def get_caller_args(caller):
    args, varargs, keywords, values = inspect.getargvalues(caller)
    output = [(i, values[i]) for i in args]
    if varargs: output.extend([(i) for i in values[varargs]])
    if keywords: output.extend([(k, v) for k, v in values[keywords].items()])
    return output

def get_func_info(level = 1):
    frame = inspect.stack()[level]
    caller = frame[0]
    function_name = frame[3]
    frame.filename
    frame.lineno
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
    return f"{function_name} ({args})"

def print_func_info():
    print(get_func_info(level = 2))
