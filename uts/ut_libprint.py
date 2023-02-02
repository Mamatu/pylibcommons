__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import datetime
import logging
import os

from pylibcommons import libprint, libgrep

import pytest
import re

def test_print_func_info_1(capsys):
    def foo(x, b):
        libprint.print_func_info(print_filename_and_linenumber_of_call = False)
    foo("a", "b")
    captured = capsys.readouterr()
    assert "foo (x = 'a', b = 'b')\n" == captured.out

def test_print_func_info_2(capsys):
    def foo():
        libprint.print_func_info(print_filename_and_linenumber_of_call = False)
    foo()
    captured = capsys.readouterr()
    assert "foo ()\n" == captured.out

def test_print_func_info_3(capsys):
    def foo(alpha, **kwargs):
        libprint.print_func_info(print_filename_and_linenumber_of_call = False)
    foo(alpha = 1, beta = 2, gamma = 3)
    captured = capsys.readouterr()
    assert "foo (alpha = 1, beta = 2, gamma = 3)\n" == captured.out

def test_print_func_info_4(capsys):
    def foo(alpha, *args, **kwargs):
        libprint.print_func_info(print_filename_and_linenumber_of_call = False)
    foo(1, 4, 5,  beta = 2, gamma = 3)
    captured = capsys.readouterr()
    assert "foo (alpha = 1, 4, 5, beta = 2, gamma = 3)\n" == captured.out

def test_add_print_func_to_methods_1(capsys):
    @libprint.print_func_info_in_methods(begin_end = False)
    class Foo:
        def __init__(self):
            self.a = 0
        def print_a(self, a = 1):
            print(self.a)
            print(a)
    foo = Foo()
    foo.print_a(a = 2)
    captured = capsys.readouterr()
    expected = [
        "__init__ (self = <ut_libprint.test_add_print_func_to_methods_1.<locals>.Foo object at .*>) .*/pyjobs/private/pylibcommons/uts/ut_libprint.py:53",
        "print_a (self = <ut_libprint.test_add_print_func_to_methods_1.<locals>.Foo object at .*>, a = 2) .*/pyjobs/private/pylibcommons/uts/ut_libprint.py:54",
        "0",
        "2"
    ]
    out = captured.out
    out = out.split("\n")
    out.remove('')
    assert len(out) == len(expected)
    for line in zip(expected, out):
        assert libgrep.grep_in_text(line[1], line[0])

def test_add_print_func_to_methods_with_begin_end_support(capsys):
    @libprint.print_func_info_in_methods(begin_end = True)
    class Foo:
        def __init__(self):
            self.a = 0
        def foo(self, a = 2):
            self.bar(a)
        def bar(self, a = 1):
            print("2")
    foo = Foo()
    foo.foo(a = 2)
    captured = capsys.readouterr()
    expected = [
        "+ __init__ (<ut_libprint.test_add_print_func_to_methods_with_begin_end_support.<locals>.Foo object at .*>) .*/pyjobs/private/pylibcommons/uts/ut_libprint.py:78",
        "- __init__ (<ut_libprint.test_add_print_func_to_methods_with_begin_end_support.<locals>.Foo object at .*>) .*/pyjobs/private/pylibcommons/uts/ut_libprint.py:78",
        "+ foo (self = <ut_libprint.test_add_print_func_to_methods_with_begin_end_support.<locals>.Foo object at .*>, a = 2) .*/pyjobs/private/pylibcommons/uts/ut_libprint.py:54",
        "+ bar (self = <ut_libprint.test_add_print_func_to_methods_with_begin_end_support.<locals>.Foo object at .*>, a = 2) .*/pyjobs/private/pylibcommons/uts/ut_libprint.py:54",
        "- bar (self = <ut_libprint.test_add_print_func_to_methods_with_begin_end_support.<locals>.Foo object at .*>, a = 2) .*/pyjobs/private/pylibcommons/uts/ut_libprint.py:54",
        "- foo (self = <ut_libprint.test_add_print_func_to_methods_with_begin_end_support.<locals>.Foo object at .*>, a = 2) .*/pyjobs/private/pylibcommons/uts/ut_libprint.py:54",
        "0",
    ]
    out = captured.out
    out = out.split("\n")
    out.remove('')
    assert len(out) == len(expected)
    for line in zip(expected, out):
        assert libgrep.grep_in_text(line[1], line[0])
