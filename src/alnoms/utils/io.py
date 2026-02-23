"""
Input/Output Utilities for Test Data.

This module provides utility functions to load large test datasets from files.
It is designed to handle common formats used in algorithm testing, such as
whitespace-separated integers (for sorting) or strings (for tries/searching).

Functions:
    - read_all_ints: Reads all integers from a file (whitespace-separated).
    - read_all_strings: Reads all string tokens from a file (whitespace-separated).
    - read_lines: Reads all lines from a file, stripping whitespace.

Usage:
    >>> from alnoms.algos.utils.io import read_all_ints
    >>> data = read_all_ints("tests/data/1Kints.txt")
"""

import os
from typing import List


def read_all_ints(path: str) -> List[int]:
    """
    Reads all integers from the specified file.

    The file is expected to contain integers separated by any amount of
    whitespace (spaces, tabs, newlines). This is the standard format for
    sorting and searching benchmarks.

    Args:
        path (str): The absolute or relative path to the file.

    Returns:
        List[int]: A list of all integers found in the file.

    Raises:
        FileNotFoundError: If the file path does not exist.
        ValueError: If the file contains tokens that cannot be parsed as integers.
    """
    _validate_path(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        # split() with no arguments splits by any whitespace run (space, tab, \n)
        tokens = content.split()
        return [int(token) for token in tokens]


def read_all_strings(path: str) -> List[str]:
    """
    Reads all whitespace-separated strings from the specified file.

    Useful for loading data for Trie tests or String Sorts (MSD/LSD).

    Args:
        path (str): The absolute or relative path to the file.

    Returns:
        List[str]: A list of all string tokens found in the file.

    Raises:
        FileNotFoundError: If the file path does not exist.
    """
    _validate_path(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        return content.split()


def read_lines(path: str) -> List[str]:
    """
    Reads all lines from the file, stripping leading and trailing whitespace.

    Preserves empty lines as empty strings.

    Args:
        path (str): The absolute or relative path to the file.

    Returns:
        List[str]: A list of lines.

    Raises:
        FileNotFoundError: If the file path does not exist.
    """
    _validate_path(path)
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            lines.append(line.strip())
    return lines


def _validate_path(path: str) -> None:
    """Helper to validate file existence."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
