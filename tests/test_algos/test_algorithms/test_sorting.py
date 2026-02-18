import pytest
from arprax.algos.algorithms.sorting import (
    selection_sort,
    insertion_sort,
    shell_sort,
    merge_sort,
    quick_sort,
    heap_sort,
)

# List of all sort functions to parametrize tests
SORTS = [selection_sort, insertion_sort, shell_sort, merge_sort, quick_sort, heap_sort]


@pytest.mark.parametrize("sort_func", SORTS)
def test_standard_sort(sort_func):
    """Test standard sorting functionality."""
    # Random data
    arr = [5, 2, 9, 1, 5, 6]
    sorted_arr = sort_func(arr, visualize=False)
    assert sorted_arr == [1, 2, 5, 5, 6, 9]

    # Already sorted
    assert sort_func([1, 2, 3]) == [1, 2, 3]

    # Reverse
    assert sort_func([3, 2, 1]) == [1, 2, 3]

    # Empty
    assert sort_func([]) == []


@pytest.mark.parametrize("sort_func", SORTS)
def test_visualizer_mode(sort_func):
    """Test that visualize=True returns a generator yielding states."""
    arr = [3, 2, 1]
    gen = sort_func(arr, visualize=True)

    # Consuming the generator should yield lists
    states = list(gen)

    # Must yield at least one state
    assert len(states) > 0

    # The final state must be sorted
    assert states[-1] == [1, 2, 3]

    # Check intermediate state is valid list
    assert isinstance(states[0], list)


def test_quick_sort_duplicates():
    """Specific test for 3-way partitioning efficiency logic."""
    arr = [2, 2, 2, 1, 3, 2]
    sorted_arr = quick_sort(arr)
    assert sorted_arr == [1, 2, 2, 2, 2, 3]
