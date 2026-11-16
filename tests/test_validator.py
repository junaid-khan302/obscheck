from validator import validate_line, is_valid_time


def test_valid_line():
    result = validate_line("09:00:05;S01;Passive;Obs1")
    assert result["status"] == "Valid"
    assert result["messages"] == []


def test_lowercase_activity_is_warning():
    result = validate_line("09:00:10;S02;active;Obs1")
    assert result["status"] == "Warning"


def test_missing_observer_is_warning():
    result = validate_line("09:00:15;S01;Constructive")
    assert result["status"] == "Warning"


def test_impossible_time_is_error():
    result = validate_line("25:99:00;S03;Interactive;Obs1")
    assert result["status"] == "Error"


def test_empty_student_is_error():
    result = validate_line("09:00:25;;Passive;Obs1")
    assert result["status"] == "Error"


def test_unknown_activity_is_error():
    result = validate_line("09:00:30;S02;Sleeping;Obs1")
    assert result["status"] == "Error"


def test_extra_spaces_is_warning():
    result = validate_line("09:00:35;S03; Active ;Obs1")
    assert result["status"] == "Warning"


def test_garbage_line_is_error():
    result = validate_line("this line is garbage")
    assert result["status"] == "Error"


def test_is_valid_time():
    assert is_valid_time("23:59:59") is True
    assert is_valid_time("24:00:00") is False
    assert is_valid_time("9:00:05") is False