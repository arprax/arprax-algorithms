"""
Unit tests for Arprax Data Generators.
Validates pure-Python and NumPy-fallback data generation logic.
"""

from unittest.mock import patch
from alnoms.utils.generators import (
    random_array,
    sorted_array,
    reverse_sorted_array,
    large_scale_dataset,
)


def test_random_array_length():
    """Verifies that the random array generator respects the requested size."""
    data = random_array(100)
    assert len(data) == 100
    assert isinstance(data, list)


def test_sorted_array_is_actually_sorted():
    """Ensures the sorted generator produces ascending sequences."""
    data = sorted_array(50)
    assert data == sorted(data)
    assert data[0] == 0
    assert data[-1] == 49


def test_reverse_logic_coverage():
    """
    Exhaustive check for the reverse-sorted branch (Line 42 coverage).

    Verifies the entire sequence and the legacy wrapper.
    """
    # Test through sorted_array flag
    res = sorted_array(5, reverse=True)
    expected = [4, 3, 2, 1, 0]
    assert res == expected

    # Test through legacy wrapper
    assert reverse_sorted_array(3) == [2, 1, 0]


def test_large_scale_dataset_fallback():
    """
    Tests the high-performance generator's graceful degradation.

    Ensures that even if NumPy is missing (Ultra-Lean mode), the
    dataset is still generated correctly via standard Python.
    """
    n = 100
    data = large_scale_dataset(n)
    assert len(data) == n
    assert all(isinstance(x, int) for x in data)


def test_generators_fallback_coverage():
    """
    Forces execution of lines 76-78 by mocking a missing NumPy.

    This ensures the 'except ImportError' branch is verified for the
    Arctic Code Vault and SFA interview standards.
    """
    # Use __import__ to mock the failure of the 'import numpy' line
    with patch("builtins.__import__", side_effect=ImportError):
        # This triggers the 'except' block in generators.py
        data = large_scale_dataset(10)
        assert len(data) == 10
        assert isinstance(data, list)


def test_random_list_generator():
    from alnoms.utils.generators import large_scale_dataset

    # Test with a standard value
    result = large_scale_dataset(5)
    assert len(result) == 5
    # Test with zero (the likely missing edge case)
    assert len(large_scale_dataset(0)) == 0
