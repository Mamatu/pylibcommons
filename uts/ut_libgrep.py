from pylibcommons import libgrep
from pylibcommons.private.libtempfile import create_temp_file

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

def test_grep_line_regex_with_line_two_lines():
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

def _open_temp_file(mode = "w+", data = None):
    import tempfile
    f = tempfile.NamedTemporaryFile(mode = mode)
    if data and "w" in mode:
        f.write(data)
        f.flush()
    elif data:
        raise Exception("If any data to write then mode must be w")
    return f

