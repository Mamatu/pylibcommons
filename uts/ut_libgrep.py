from pylibcommons import libgrep
from pylibcommons.private.libtemp import create_temp_file, create_temp_dir

from unittest.mock import patch

import pytest
import os

@patch("os.listdir")
@patch("os.path.isfile")
def test_handle_directory_1(os_path_isfile, os_listdir_mock):
    os_path_isfile.return_value = True
    os_listdir_mock.return_value = ["1", "10", "2"]
    assert ["/tmp/1", "/tmp/2", "/tmp/10"] == libgrep.get_directory_content("/tmp/")

@patch("os.listdir")
@patch("os.path.isfile")
def test_handle_directory_2(os_path_isfile, os_listdir_mock):
    os_path_isfile.return_value = True
    os_listdir_mock.return_value = ["1", "10", "2", "a"]
    assert ["/tmp/a", "/tmp/1", "/tmp/2", "/tmp/10"] == libgrep.get_directory_content("/tmp/")

def test_grep_in_directory_line1():
    data = {}
    data["0"] = "2021-12-19 17:59:17.171 line1\n"
    data["0"] += "2021-12-19 17:59:17.172 line2\n"
    data["0"] += "2021-12-19 17:59:17.173 line3\n"
    data["0"] += "2021-12-19 17:59:17.173 line4\n"
    data["1"] = "2021-12-19 17:59:17.175 line5\n"
    data["1"] += "2021-12-19 17:59:17.176 line6\n"
    data["1"] += "2021-12-19 17:59:17.177 line7\n"
    data["1"] += "2021-12-19 17:59:17.177 line8\n"
    data["2"] = "2021-12-19 17:59:17.179 line9\n"
    data["2"] += "2021-12-19 17:59:17.180 line10\n"
    data["2"] += "2021-12-19 17:59:17.181 line11\n"
    data["2"] += "2021-12-19 17:59:17.181 line12\n"
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    with create_temp_dir(data = data) as _dir:
        out = libgrep.grep_regex_in_line(_dir, "line1\\>", line_regex, support_directory = True)
        assert 1 == len(out)
        assert 1 == out[0].line_number
        assert "2021-12-19 17:59:17.171" == out[0].matched[0]
        assert os.path.join(_dir, "0") == out[0].filepath

def test_grep_in_directory_line2():
    data = {}
    data["0"] = "2021-12-19 17:59:17.171 line1\n"
    data["0"] += "2021-12-19 17:59:17.172 line2\n"
    data["0"] += "2021-12-19 17:59:17.173 line3\n"
    data["0"] += "2021-12-19 17:59:17.173 line4\n"
    data["1"] = "2021-12-19 17:59:17.175 line5\n"
    data["1"] += "2021-12-19 17:59:17.176 line6\n"
    data["1"] += "2021-12-19 17:59:17.177 line7\n"
    data["1"] += "2021-12-19 17:59:17.177 line8\n"
    data["2"] = "2021-12-19 17:59:17.179 line9\n"
    data["2"] += "2021-12-19 17:59:17.180 line10\n"
    data["2"] += "2021-12-19 17:59:17.181 line11\n"
    data["2"] += "2021-12-19 17:59:17.182 line12\n"
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    with create_temp_dir(data = data) as _dir:
        out = libgrep.grep_regex_in_line(_dir, "line2", line_regex, support_directory = True)
        assert 1 == len(out)
        assert 2 == out[0].line_number
        assert "2021-12-19 17:59:17.172" == out[0].matched[0]
        assert os.path.join(_dir, "0") == out[0].filepath

def test_grep_in_directory_line6():
    data = {}
    data["0"] = "2021-12-19 17:59:17.171 line1\n"
    data["0"] += "2021-12-19 17:59:17.172 line2\n"
    data["0"] += "2021-12-19 17:59:17.173 line3\n"
    data["0"] += "2021-12-19 17:59:17.173 line4\n"
    data["1"] = "2021-12-19 17:59:17.175 line5\n"
    data["1"] += "2021-12-19 17:59:17.176 line6\n"
    data["1"] += "2021-12-19 17:59:17.177 line7\n"
    data["1"] += "2021-12-19 17:59:17.177 line8\n"
    data["2"] = "2021-12-19 17:59:17.179 line9\n"
    data["2"] += "2021-12-19 17:59:17.180 line10\n"
    data["2"] += "2021-12-19 17:59:17.181 line11\n"
    data["2"] += "2021-12-19 17:59:17.182 line12\n"
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    with create_temp_dir(data = data) as _dir:
        out = libgrep.grep_regex_in_line(_dir, "line6", line_regex, support_directory = True)
        assert 1 == len(out)
        assert 2 == out[0].line_number
        assert "2021-12-19 17:59:17.176" == out[0].matched[0]
        assert os.path.join(_dir, "1") == out[0].filepath

def test_grep_in_directory_line12():
    data = {}
    data["0"] = "2021-12-19 17:59:17.171 line1\n"
    data["0"] += "2021-12-19 17:59:17.172 line2\n"
    data["0"] += "2021-12-19 17:59:17.173 line3\n"
    data["0"] += "2021-12-19 17:59:17.173 line4\n"
    data["1"] = "2021-12-19 17:59:17.175 line5\n"
    data["1"] += "2021-12-19 17:59:17.176 line6\n"
    data["1"] += "2021-12-19 17:59:17.177 line7\n"
    data["1"] += "2021-12-19 17:59:17.177 line8\n"
    data["2"] = "2021-12-19 17:59:17.179 line9\n"
    data["2"] += "2021-12-19 17:59:17.180 line10\n"
    data["2"] += "2021-12-19 17:59:17.181 line11\n"
    data["2"] += "2021-12-19 17:59:17.182 line12\n"
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    with create_temp_dir(data = data) as _dir:
        out = libgrep.grep_regex_in_line(_dir, "line12", line_regex, support_directory = True)
        assert 1 == len(out)
        assert 4 == out[0].line_number
        assert "2021-12-19 17:59:17.182" == out[0].matched[0]
        assert os.path.join(_dir, "2") == out[0].filepath

def test_grep_line_regex_with_line_two_lines():
    test_file = create_temp_file()
    testfile_path = test_file.name
    with open(testfile_path, "w") as f:
        f.write("regex\n")
        f.write("2021-12-19 17:59:17.171 [ 15] I regex\n")
        f.write("regex\n")
        f.write("2021-12-19 17:59:17.172 [ 15] I regex\n")
        f.write("regex")
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    out = libgrep.grep_regex_in_line(testfile_path, "regex", line_regex)
    assert 2 == len(out)
    assert 2 == out[0].line_number
    assert 4 == out[1].line_number
    assert "2021-12-19 17:59:17.171" == out[0].matched[0]
    assert "2021-12-19 17:59:17.172" == out[1].matched[0]

def test_grep_line_regex_from_line_1():
    test_file = create_temp_file()
    testfile_path = test_file.name
    with open(testfile_path, "w") as f:
        f.write("2021-12-19 17:59:17.171 [ 15] I regex\n")
        f.write("2021-12-19 17:59:17.172 [ 15] I line\n")
        f.write("2021-12-19 17:59:17.173 [ 15] I line\n")
        f.write("2021-12-19 17:59:17.174 [ 15] I line\n")
        f.write("2021-12-19 17:59:17.175 [ 15] I regex\n")
        f.write("2021-12-19 17:59:17.176 [ 15] I line\n")
        f.write("2021-12-19 17:59:17.177 [ 15] I line\n")
        f.write("2021-12-19 17:59:17.178 [ 15] I line")
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    out = libgrep.grep_regex_in_line(testfile_path, "regex", line_regex, fromLine = 3)
    assert 1 == len(out)
    assert 5 == out[0].line_number

def test_grep_line_regex_from_line_2():
    test_file = create_temp_file()
    testfile_path = test_file.name
    with open(testfile_path, "w") as f:
        f.write("2021-12-19 17:59:17.171 [ 15] I regex1\n")
        f.write("2021-12-19 17:59:17.172 [ 15] I line\n")
        f.write("2021-12-19 17:59:17.173 [ 15] I line\n")
        f.write("2021-12-19 17:59:17.174 [ 15] I line\n")
        f.write("2021-12-19 17:59:17.175 [ 15] I regex2\n")
        f.write("2021-12-19 17:59:17.176 [ 15] I regex3\n")
        f.write("2021-12-19 17:59:17.177 [ 15] I line\n")
        f.write("2021-12-19 17:59:17.178 [ 15] I line\n")
        f.write("2021-12-19 17:59:17.179 [ 15] I line")
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    out = libgrep.grep_regex_in_line(testfile_path, "regex", line_regex, fromLine = 5)
    assert 2 == len(out)
    assert 5 == out[0].line_number
    assert 6 == out[1].line_number
    assert "2021-12-19 17:59:17.175" == out[0].matched[0]
    assert "2021-12-19 17:59:17.176" == out[1].matched[0]

def test_grep_one_regex_repeated():
    test_file = create_temp_file()
    testfile_path = test_file.name
    with open(testfile_path, "w") as f:
        f.write("ada\nada\nada")
    out = libgrep.grep(testfile_path, "ada")
    assert len(out) == 3
    assert "ada" == out[0].matched
    assert "ada" == out[1].matched
    assert "ada" == out[2].matched

def test_grep_one_regex_in_bias():
    test_file = create_temp_file()
    testfile_path = test_file.name
    with open(testfile_path, "w") as f:
        f.write("ada\ndud\nada\ndud\nada\nada")
    out = libgrep.grep(testfile_path, "ada")
    assert len(out) == 4
    assert "ada" == out[0].matched
    assert 1 == out[0].line_number
    assert "ada" == out[1].matched
    assert 3 == out[1].line_number
    assert "ada" == out[2].matched
    assert 5 == out[2].line_number
    assert "ada" == out[3].matched
    assert 6 == out[3].line_number

def test_grep_line_regex_with_line_number():
    test_file = create_temp_file()
    testfile_path = test_file.name
    with open(testfile_path, "w") as f:
        f.write("2021-12-19 17:59:17.171 [ 15] I start")
        f.write("\n")
        f.write("2021-12-19 17:59:17.172 [ 15] I end")
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    out = libgrep.grep_regex_in_line(testfile_path, "start", line_regex)
    assert 1 == out[0].line_number
    assert "2021-12-19 17:59:17.171" == out[0].matched[0]
    assert len(out) == 1
    out = libgrep.grep_regex_in_line(testfile_path, "end", line_regex)
    assert 2 == out[0].line_number
    assert "2021-12-19 17:59:17.172" == out[0].matched[0]
    assert len(out) == 1

def test_grep_line_regex_with_line_two_lines_1():
    test_file = create_temp_file()
    testfile_path = test_file.name
    with open(testfile_path, "w") as f:
        f.write("2021-12-19 17:59:17.171 [ 15] I regex")
        f.write("\n")
        f.write("2021-12-19 17:59:17.172 [ 15] I regex")
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    out = libgrep.grep_regex_in_line(testfile_path, "regex", line_regex)
    assert 2 == len(out)
    assert 1 == out[0].line_number
    assert 2 == out[1].line_number
    assert "2021-12-19 17:59:17.171" == out[0].matched[0]
    assert "2021-12-19 17:59:17.172" == out[1].matched[0]

def test_grep_empty():
    test_file = create_temp_file()
    testfile_path = test_file.name
    with open(testfile_path, "w") as f:
        f.write("")
    out = libgrep.grep(testfile_path, "2")
    assert [] == out

def test_grep():
    test_file = create_temp_file()
    testfile_path = test_file.name
    assert isinstance(testfile_path, str)
    with open(testfile_path, "w") as f:
        f.write("1\n2")
    out = libgrep.grep(testfile_path, "2")
    assert (len(out) == 1)
    assert ("2" == out[0].matched)

def test_grep_in_text():
    out = libgrep.grep_in_text("2021-12-19 17:59:17.171 line1", "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-9]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}", only_match = True)
    assert (len(out) == 1)
    assert ("2021-12-19 17:59:17.171" == out[0].matched)

def test_get_file_line_number_1():
    data = {}
    data["0"] = "2021-12-19 17:59:17.171 line1\n"
    data["0"] += "2021-12-19 17:59:17.172 line2\n"
    data["0"] += "2021-12-19 17:59:17.173 line3\n"
    data["0"] += "2021-12-19 17:59:17.173 line4\n"
    data["1"] = "2021-12-19 17:59:17.175 line5\n"
    data["1"] += "2021-12-19 17:59:17.176 line6\n"
    data["1"] += "2021-12-19 17:59:17.177 line7\n"
    data["1"] += "2021-12-19 17:59:17.177 line8\n"
    data["2"] = "2021-12-19 17:59:17.179 line9\n"
    data["2"] += "2021-12-19 17:59:17.180 line10\n"
    data["2"] += "2021-12-19 17:59:17.181 line11\n"
    data["2"] += "2021-12-19 17:59:17.181 line12\n"
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    with create_temp_dir(data = data) as _dir:
        out = libgrep.grep_regex_in_line(_dir, "line1\\>", line_regex, support_directory = True)
        assert 1 == len(out)
        assert 1 == out[0].line_number
        file_line_number = out[0].get_file_line_number()
        assert 1 == file_line_number.line_number
        assert 0 == file_line_number.file_number
        assert "2021-12-19 17:59:17.171" == out[0].matched[0]
        assert os.path.join(_dir, "0") == out[0].filepath

def test_get_file_line_number_2():
    data = {}
    data["0"] = "2021-12-19 17:59:17.171 line1\n"
    data["0"] += "2021-12-19 17:59:17.172 line2\n"
    data["0"] += "2021-12-19 17:59:17.173 line3\n"
    data["0"] += "2021-12-19 17:59:17.173 line4\n"
    data["1"] = "2021-12-19 17:59:17.175 line5\n"
    data["1"] += "2021-12-19 17:59:17.176 line6\n"
    data["1"] += "2021-12-19 17:59:17.177 line7\n"
    data["1"] += "2021-12-19 17:59:17.177 line8\n"
    data["2"] = "2021-12-19 17:59:17.179 line9\n"
    data["2"] += "2021-12-19 17:59:17.180 line10\n"
    data["2"] += "2021-12-19 17:59:17.181 line11\n"
    data["2"] += "2021-12-19 17:59:17.181 line12\n"
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    with create_temp_dir(data = data) as _dir:
        out1 = libgrep.grep_regex_in_line(_dir, "line1\\>", line_regex, support_directory = True)
        out2 = libgrep.grep_regex_in_line(_dir, "line9\\>", line_regex, support_directory = True)
        fln1 = out1[0].get_file_line_number()
        fln2 = out2[0].get_file_line_number()
        assert fln1.line_number == fln2.line_number
        assert fln1.file_number != fln2.file_number
        assert fln1 < fln2
        assert fln2 > fln1
        assert fln1 == fln1
        assert fln1 >= fln1
        assert fln1 <= fln1
        assert fln2 == fln2
        assert fln2 >= fln2
        assert fln2 <= fln2

def test_get_file_line_number_3():
    data = {}
    data["0"] = "2021-12-19 17:59:17.171 line1\n"
    data["0"] += "2021-12-19 17:59:17.172 line2\n"
    data["0"] += "2021-12-19 17:59:17.173 line3\n"
    data["0"] += "2021-12-19 17:59:17.173 line4\n"
    data["1"] = "2021-12-19 17:59:17.175 line5\n"
    data["1"] += "2021-12-19 17:59:17.176 line6\n"
    data["1"] += "2021-12-19 17:59:17.177 line7\n"
    data["1"] += "2021-12-19 17:59:17.177 line8\n"
    data["2"] = "2021-12-19 17:59:17.179 line9\n"
    data["2"] += "2021-12-19 17:59:17.180 line10\n"
    data["2"] += "2021-12-19 17:59:17.181 line11\n"
    data["2"] += "2021-12-19 17:59:17.181 line12\n"
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    with create_temp_dir(data = data) as _dir:
        out1 = libgrep.grep_regex_in_line(_dir, "line1\\>", line_regex, support_directory = True)
        out2 = libgrep.grep_regex_in_line(_dir, "line4\\>", line_regex, support_directory = True)
        fln1 = out1[0].get_file_line_number()
        fln2 = out2[0].get_file_line_number()
        assert fln1.line_number != fln2.line_number
        assert fln1.file_number == fln2.file_number
        assert fln1 < fln2
        assert fln2 > fln1
        assert fln1 == fln1
        assert fln1 >= fln1
        assert fln1 <= fln1
        assert fln2 == fln2
        assert fln2 >= fln2
        assert fln2 <= fln2

def test_get_file_line_number_4():
    data = {}
    data["file_0"] = "2021-12-19 17:59:17.171 line1\n"
    data["file_0"] += "2021-12-19 17:59:17.172 line2\n"
    data["file_0"] += "2021-12-19 17:59:17.173 line3\n"
    data["file_0"] += "2021-12-19 17:59:17.173 line4\n"
    data["file_1"] = "2021-12-19 17:59:17.175 line5\n"
    data["file_1"] += "2021-12-19 17:59:17.176 line6\n"
    data["file_1"] += "2021-12-19 17:59:17.177 line7\n"
    data["file_1"] += "2021-12-19 17:59:17.177 line8\n"
    data["file_2"] = "2021-12-19 17:59:17.179 line9\n"
    data["file_2"] += "2021-12-19 17:59:17.180 line10\n"
    data["file_2"] += "2021-12-19 17:59:17.181 line11\n"
    data["file_2"] += "2021-12-19 17:59:17.181 line12\n"
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    with create_temp_dir(data = data) as _dir:
        out1 = libgrep.grep_regex_in_line(_dir, "line1\\>", line_regex, support_directory = True)
        out2 = libgrep.grep_regex_in_line(_dir, "line4\\>", line_regex, support_directory = True)
        fln1 = out1[0].get_file_line_number()
        fln2 = out2[0].get_file_line_number()
        assert fln1.line_number != fln2.line_number
        assert fln1.file_number == fln2.file_number
        assert fln1 < fln2
        assert fln2 > fln1
        assert fln1 == fln1
        assert fln1 >= fln1
        assert fln1 <= fln1
        assert fln2 == fln2
        assert fln2 >= fln2
        assert fln2 <= fln2

def test_get_file_line_number_5():
    data = {}
    data["file_0"] = "2021-12-19 17:59:17.171 line1\n"
    data["file_0"] += "2021-12-19 17:59:17.172 line2\n"
    data["file_0"] += "2021-12-19 17:59:17.173 line3\n"
    data["file_0"] += "2021-12-19 17:59:17.173 line4\n"
    data["file_1"] = "2021-12-19 17:59:17.175 line5\n"
    data["file_1"] += "2021-12-19 17:59:17.176 line6\n"
    data["file_1"] += "2021-12-19 17:59:17.177 line7\n"
    data["file_1"] += "2021-12-19 17:59:17.177 line8\n"
    data["file_2"] = "2021-12-19 17:59:17.179 line9\n"
    data["file_2"] += "2021-12-19 17:59:17.180 line10\n"
    data["file_2"] += "2021-12-19 17:59:17.181 line11\n"
    data["file_2"] += "2021-12-19 17:59:17.181 line12\n"
    line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    with create_temp_dir(data = data) as _dir:
        out1 = libgrep.grep_regex_in_line(_dir, "line1\\>", line_regex, support_directory = True)
        out2 = libgrep.grep_regex_in_line(_dir, "line5\\>", line_regex, support_directory = True)
        fln1 = out1[0].get_file_line_number()
        fln2 = out2[0].get_file_line_number()
        assert fln1.line_number == fln2.line_number
        assert fln1.file_number is None
        assert fln2.file_number is None
        with pytest.raises(libgrep.FileNotEqualException):
            assert fln1 < fln2
        with pytest.raises(libgrep.FileNotEqualException):
            assert fln1 < fln2
        with pytest.raises(libgrep.FileNotEqualException):
            assert fln2 > fln1
            assert fln1 == fln1
            assert fln1 >= fln1
            assert fln1 <= fln1
            assert not fln1 != fln1
            assert not fln1 > fln1
            assert not fln1 < fln1
            assert fln2 == fln2
            assert fln2 >= fln2
            assert fln2 <= fln2
            assert not fln2 != fln2
            assert not fln2 > fln2
            assert not fln2 < fln2
