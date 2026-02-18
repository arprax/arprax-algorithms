import pytest
from arprax.algos.algorithms.searching import binary_search, rank, quick_select


# --- Binary Search Tests ---


def test_binary_search_basic():
    a = [10, 20, 30, 40, 50]
    assert binary_search(a, 30) == 2
    assert binary_search(a, 10) == 0
    assert binary_search(a, 50) == 4


def test_binary_search_missing():
    a = [1, 3, 5]
    assert binary_search(a, 2) == -1
    assert binary_search(a, 0) == -1
    assert binary_search(a, 6) == -1


def test_binary_search_empty():
    assert binary_search([], 10) == -1


# --- Rank Tests ---


def test_rank_basic():
    # Rank = "How many elements are strictly less than Key?"
    a = [10, 20, 30, 40, 50]
    assert rank(a, 30) == 2  # 10, 20 are smaller
    assert rank(a, 10) == 0
    assert rank(a, 55) == 5  # All 5 are smaller


def test_rank_insertion_point():
    # Key 25 doesn't exist. 10, 20 are smaller.
    a = [10, 20, 30]
    assert rank(a, 25) == 2
    assert rank(a, 5) == 0


def test_rank_duplicates():
    # Should return index of FIRST occurrence
    a = [10, 20, 20, 20, 30]
    assert rank(a, 20) == 1


# --- Quick Select Tests ---


def test_quick_select_basic():
    # Unsorted: [50, 20, 10, 40, 30]
    # Sorted:   [10, 20, 30, 40, 50]
    a = [50, 20, 10, 40, 30]

    assert quick_select(a, 0) == 10  # Min
    assert quick_select(a, 2) == 30  # Median
    assert quick_select(a, 4) == 50  # Max


def test_quick_select_large():
    # Find median of 0..99
    a = list(range(100))
    import random

    random.shuffle(a)

    assert quick_select(a, 50) == 50


def test_quick_select_errors():
    a = [1, 2, 3]
    with pytest.raises(ValueError):
        quick_select(a, -1)
    with pytest.raises(ValueError):
        quick_select(a, 10)
