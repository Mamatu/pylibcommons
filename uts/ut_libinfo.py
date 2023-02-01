__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import datetime
import logging
import os

from pylibcommons import libinfo

import pytest

def test_self_detection(capsys):
    class Foo:
        def foo1(self, x, b):
            caller = libinfo.get_caller_from_frame_or_level(1)
            args = libinfo.get_caller_args(caller)
            print(caller)
            print(caller.f_locals)
            print(caller.f_code.co_name)
            print(dir(caller.f_code))
            print(args)
    def foo(x, b):
        caller = libinfo.get_caller_from_frame_or_level(1)
        args = libinfo.get_caller_args(caller)
        assert not hasattr(caller, "__self__")
        print(args)
    #foo("a", "b")
    foo = Foo()
    foo.foo1("a", "b")
    #captured = capsys.readouterr()
    #assert "foo (x = 'a', b = 'b')\n" == captured.out

def test_print_func_info_1(capsys):
    def foo(x, b):
        libinfo.print_func_info(print_filename_and_linenumber_of_call = False)
    foo("a", "b")
    captured = capsys.readouterr()
    assert "foo (x = 'a', b = 'b')\n" == captured.out

def test_print_func_info_2(capsys):
    def foo():
        libinfo.print_func_info(print_filename_and_linenumber_of_call = False)
    foo()
    captured = capsys.readouterr()
    assert "foo ()\n" == captured.out

def test_print_func_info_3(capsys):
    def foo(alpha, **kwargs):
        libinfo.print_func_info(print_filename_and_linenumber_of_call = False)
    foo(alpha = 1, beta = 2, gamma = 3)
    captured = capsys.readouterr()
    assert "foo (alpha = 1, beta = 2, gamma = 3)\n" == captured.out

def test_print_func_info_4(capsys):
    def foo(alpha, *args, **kwargs):
        libinfo.print_func_info(print_filename_and_linenumber_of_call = False)
    foo(1, 4, 5,  beta = 2, gamma = 3)
    captured = capsys.readouterr()
    assert "foo (alpha = 1, 4, 5, beta = 2, gamma = 3)\n" == captured.out

def test_add_print_func_to_methods_1(capsys):
    @libinfo.print_func_info_in_methods()
    class Foo:
        def __init__(self):
            self.a = 0
        def print_a(self, a = 1):
            print(self.a)
            print(a)
    foo = Foo()
    foo.print_a(a = 2)
    captured = capsys.readouterr()
    assert "print_a (self, a = 2)\n" == captured.out
