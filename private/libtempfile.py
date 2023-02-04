def create_temp_file(mode = "w+", data = None):
    import tempfile
    f = tempfile.NamedTemporaryFile(mode = mode)
    if data and "w" in mode:
        f.write(data)
        f.flush()
    elif data:
        raise Exception("If any data to write then mode must be w")
    return f

