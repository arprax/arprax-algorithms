import pytest
from alnoms.utils.io import read_all_ints, read_all_strings, read_lines


def test_read_ints_valid(tmp_path):
    """Test reading integers with various whitespace."""
    # Create a temporary file using pytest's tmp_path fixture
    d = tmp_path / "data"
    d.mkdir()
    p = d / "ints.txt"
    # Write content: spaces, newlines, tabs
    p.write_text("10 20\n30   40\n\n50")

    # We must pass the string path to the function
    data = read_all_ints(str(p))
    assert data == [10, 20, 30, 40, 50]


def test_read_ints_invalid(tmp_path):
    """Test handling of non-integer data."""
    p = tmp_path / "bad_ints.txt"
    p.write_text("10 twenty 30")

    with pytest.raises(ValueError):
        read_all_ints(str(p))


def test_read_strings(tmp_path):
    """Test reading strings."""
    p = tmp_path / "strings.txt"
    p.write_text("hello world\n  python  Algorithm ")

    data = read_all_strings(str(p))
    assert data == ["hello", "world", "python", "Algorithm"]


def test_read_lines(tmp_path):
    """Test reading lines with stripping."""
    p = tmp_path / "lines.txt"
    # Line 1: Normal
    # Line 2: Leading/Trailing space
    # Line 3: Empty (Newlines)
    p.write_text("Line 1\n  Line 2  \n\nLine 4")

    data = read_lines(str(p))
    assert len(data) == 4
    assert data[0] == "Line 1"
    assert data[1] == "Line 2"
    assert data[2] == ""  # Empty line remains empty string
    assert data[3] == "Line 4"


def test_file_not_found():
    """Test non-existent file error."""
    with pytest.raises(FileNotFoundError):
        read_all_ints("ghost_file_does_not_exist.txt")
