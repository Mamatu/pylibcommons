def handle_kwargs(keys, default_output = None, is_required = False, **kwargs):
    if isinstance(keys, str):
        return handle_kwargs([keys], default_output = default_output, is_required = is_required, **kwargs)
    keys_in_kwargs = [k for k in keys if k in kwargs]
    if len(keys_in_kwargs) > 1:
        raise Exception(f"Only one alternative {keys_in_kwargs} can be parameter")
    if len(keys_in_kwargs) == 0:
        if is_required:
            raise Exception(f"Arg {keys} is required")
        return default_output
    return kwargs[keys_in_kwargs[0]]

