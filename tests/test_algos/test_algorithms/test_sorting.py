"""
Unit tests for Arprax Sorting Algorithms.
Validates functional correctness, edge cases, and visualization generators.
"""

from arprax.algos.algorithms import merge_sort, bubble_sort, selection_sort


def test_sorting_algorithms():
    """
    Verifies that all core sorting algorithms correctly sort a standard list.

    This test ensures that the default return (visualize=False) is a sorted list.
    """
    sample = [3, 1, 4, 1, 5]
    expected = [1, 1, 3, 4, 5]

    # Hits standard return paths (Lines 33-39, 123-141)
    assert merge_sort(sample, visualize=False) == expected
    assert bubble_sort(sample, visualize=False) == expected
    assert selection_sort(sample, visualize=False) == expected


def test_sorting_empty_and_single():
    """
    Tests sorting edge cases: empty lists and single-element lists.

    Ensures algorithms handle minimal inputs without crashing or recursion errors.
    """
    assert merge_sort([]) == []
    assert merge_sort([1]) == [1]
    assert bubble_sort([]) == []
    assert selection_sort([99]) == [99]


def test_sorting_visualize_mode():
    """
    Ensures that algorithms return a generator when the visualize flag is enabled.

    This validates the 'Arprax Academy' educational hooks used by visuals.py.
    """
    data = [3, 1, 2]

    # Testing bubble_sort generator branch
    gen_bubble = bubble_sort(data, visualize=True)
    assert hasattr(gen_bubble, "__iter__")
    assert list(gen_bubble)[-1] == [1, 2, 3]

    # Testing selection_sort generator branch
    gen_selection = selection_sort(data, visualize=True)
    assert hasattr(gen_selection, "__iter__")
    assert list(gen_selection)[-1] == [1, 2, 3]

    # Testing merge_sort generator branch
    gen_merge = merge_sort(data, visualize=True)
    assert hasattr(gen_merge, "__iter__")
    assert list(gen_merge)[-1] == [1, 2, 3]


def test_bubble_sort_early_exit():
    """
    Specifically tests the early-exit optimization in bubble sort.

    This ensures that the 'if not swapped: break' branch is executed.
    """
    already_sorted = [1, 2, 3, 4, 5]
    # Hits the early exit branch for 100% coverage
    assert bubble_sort(already_sorted, visualize=False) == already_sorted
