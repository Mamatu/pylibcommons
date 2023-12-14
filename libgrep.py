__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import logging
from pylibcommons import libkw
from pylibcommons import libprocess
from pylibcommons.private.libtemp import create_temp_file

_log = logging.getLogger(__name__)

def grep(path, regex, **kwargs):
    path = __handle_path(path, **kwargs)
    outputs = []
    for p in path:
        o = __grep(p, regex, **kwargs)
        if o is not None:
            outputs = outputs + o
    return outputs

def grep_in_text(text, regex, **kwargs):
    try:
        file = create_temp_file(mode = "w+", data = text)
        return grep(file.name, regex, **kwargs)
    finally:
        file.close()

def grep_regex_in_line(path, grep_regex, match_regex, **kwargs):
    """
    :path - path for greping
    :grep_regex - regex using to match line by grep
    :match_regex - regex to extract specific data from line
    :maxCount - max count of matched, if it is -1 it will be infinity
    :fromLine - start searching from specific line
    """
    import re
    fromLine = libkw.handle_kwargs(["fromLine", "from_line"], 1, **kwargs)
    if fromLine < 1:
        raise Exception(f"Invalid fromLine value {fromLine}")
    out = grep(path, grep_regex, **kwargs)
    rec = re.compile(match_regex)
    matched_lines = []
    for o in out:
        matched = o.search_in_matched(rec)
        if matched:
            matched_lines.append(o)
    return matched_lines

class GrepOutput:
    def __init__(self, line_number, matched, line_offset, filepath):
        if line_number:
            try:
                self.line_number = int(line_number.rstrip())
                self.line_number = self.line_number + line_offset
            except Exception as ex:
                _log.error(f"{line_number} cannot be converted to int! ${ex}")
                raise ex
        self.matched = matched.rstrip()
        self.filepath = filepath
    def __getitem__(self, idx):
        if idx == 0:
            return self.line_number
        if idx == 1:
            return self.matched
        raise IndexError
    def search_in_matched(self, rec):
        self.matched = rec.search(self.matched)
        return self.matched
    def __str__(self):
        return f"({self.filepath}:{self.line_number}, {self.matched})"
    @staticmethod
    def from_split(line, line_offset, filepath):
        out = line.split(':', 1)
        return GrepOutput(out[0], out[1], line_offset, filepath)

import os

def get_directory_content(path):
    dirlist = os.listdir(path)
    dirlist = [f for f in dirlist if os.path.isfile(os.path.join(path, f))]
    numbers = []
    names = []
    for f in dirlist:
        f = __try_convert_to_int(f)
        if isinstance(f, int):
            numbers.append(f)
        else:
            names.append(f)
    numbers.sort()
    names.sort()
    outputs = names + numbers
    return [os.path.join(path, str(f)) for f in outputs]

def __try_convert_to_int(f):
    try:
        return int(f)
    except ValueError:
        return f

def __handle_path(path, **kwargs):
    if not os.path.exists(path):
        raise Exception(f"Path {path} doesn't exist")
    support_directory = libkw.handle_kwargs(["support_directory", "supportDirectory"], False, **kwargs)
    if not support_directory and os.path.isdir(path):
        raise Exception(f"Path {path} is directory - it is not supported. If should be, please use supportDirectory or support_directory = True argument")
    if support_directory and os.path.isdir(path):
        return get_directory_content(path)
    return [path]

def __cat(command, path):
    process = libprocess.Process(f"cat {path}", shell = True)
    process.start()
    process.wait()
    if process.is_stdout():
        lines = process.get_stdout().readlines()
        content = f"\n|{command} {path}|\n+++\n{lines}\n---"
        _log.info(content)

def __grep(path, regex, **kwargs):
    print(f"__grep {path}")
    fromLine = libkw.handle_kwargs(["fromLine", "from_line", "n"], default_output = 1, **kwargs)
    maxCount = libkw.handle_kwargs(["maxCount", "max_count", "m"], default_output = -1, **kwargs)
    onlyMatch = libkw.handle_kwargs(["onlyMatch", "only_match", "o"], default_output = False, **kwargs)
    pre_grep_callback = libkw.handle_kwargs(["pre_grep_callback"], default_output = None, **kwargs)
    post_grep_callback = libkw.handle_kwargs(["post_grep_callback"], default_output = None, **kwargs)
    encapsulate_grep_callback = libkw.handle_kwargs(["encapsulate_grep_callback"], default_output = None, **kwargs)
    debug_cat = libkw.handle_kwargs(["debug_cat"], default_output = False, **kwargs)
    if fromLine < 1:
        raise Exception(f"Invalid fromLine value {fromLine}")
    if maxCount < -1:
        raise Exception(f"Invalid value of maxCount {maxCount}. It should be > -1")
    lineNumber = True #hardcode
    def makeArgs(lineNumber, maxCount):
        o_arg = " -o" if onlyMatch else ""
        n_arg = " -n" if lineNumber else ""
        m_arg = " -m {maxCount}" if maxCount > -1 else ""
        return f"{o_arg}{n_arg}{m_arg}"
    import subprocess, os
    args = makeArgs(lineNumber, maxCount)
    command = f"grep -a {args} -e \"{regex}\""
    if fromLine > 1:
        command = f"sed -n '{fromLine},$p' {path} | {command}"
    else:
        command = f"{command} {path}"
    if command == None:
        raise Exception("Grep command was failed on initialization")
    def readlines(f):
        lines = f.readlines()
        line_offset = 0 if fromLine < 1 else fromLine - 1
        if not lineNumber:
            lines = [GrepOutput(matched = l, line_offset = line_offset, filepath = path) for l in lines]
        else:
            lines = [GrepOutput.from_split(l, line_offset = line_offset, filepath = path) for l in lines]
        return lines
    can_be_processed = True
    if pre_grep_callback:
        can_be_processed = pre_grep_callback(path)
    out = None
    try:
        if can_be_processed:
            def _process():
                nonlocal out, debug_cat
                _log.debug(f"{grep.__name__}: {command}")
                if debug_cat:
                    __cat(command, path)
                process = libprocess.Process(command, shell = True)
                process.start()
                process.wait()
                if process.is_stderr():
                    err_lines = process.get_stderr().readlines()
                    if err_lines is not None and len(err_lines) > 0:
                        raise Exception("\n".join(err_lines))
                if process.is_stdout():
                    out = readlines(process.get_stdout())
                if debug_cat:
                    _log.info(f"{[str(o) for o in out]}")
            if not encapsulate_grep_callback:
                _process()
            else:
                encapsulate_grep_callback(_process, path)
    finally:
        if post_grep_callback:
            post_grep_callback(path)
    return out
