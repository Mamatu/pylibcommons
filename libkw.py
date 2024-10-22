__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

def handle_kwargs(keys, default_output = None, is_required = False, return_alternative = False, **kwargs):
    if isinstance(keys, str):
        return handle_kwargs([keys], default_output = default_output, is_required = is_required, **kwargs)
    keys_in_kwargs = [k for k in keys if k in kwargs]
    if len(keys_in_kwargs) > 1:
        raise Exception(f"Only one alternative {keys_in_kwargs} can be parameter")
    if len(keys_in_kwargs) == 0:
        if is_required:
            raise Exception(f"Arg {keys} is required")
        if len(keys) > 1 and return_alternative:
            return default_output, None
        return default_output
    if len(keys) > 1 and return_alternative:
        return kwargs[keys_in_kwargs[0]], keys_in_kwargs[0]
    return kwargs[keys_in_kwargs[0]]
