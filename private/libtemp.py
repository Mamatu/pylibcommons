def create_temp_file(mode = "w+", data = None):
    import tempfile
    f = tempfile.NamedTemporaryFile(mode = mode)
    if data and "w" in mode:
        f.write(data)
        f.flush()
    elif data:
        raise Exception("If any data to write then mode must be w")
    return f

def create_temp_dir(dir = None, data = None):
    import tempfile
    import os
    _dir = tempfile.TemporaryDirectory(dir = dir)
    if data and isinstance(data, dict):
        for d in data.items():
            print(d[0])
            print(d[1])
            with open(os.path.join(_dir.name, d[0]), "w+") as f:
                f.write(d[1])
                f.flush()
    return _dir
