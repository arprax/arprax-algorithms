from arprax.algos.utils.generators import random_array, sorted_array

def test_random_array_length():
    data = random_array(100)
    assert len(data) == 100

def test_sorted_array_is_actually_sorted():
    data = sorted_array(50)
    assert data == sorted(data)


def test_reverse_generator():
    # 1. Trigger the logic for 100% coverage
    arr = sorted_array(10, reverse=True)

    # 2. Strict assertion: verifies the entire sequence, not just the ends
    expected = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert arr == expected

def test_reverse_branch():
    """Verify the reverse branch for 100% coverage."""
    res = sorted_array(5, reverse=True)
    assert res == [4, 3, 2, 1, 0]

def test_sorted_array_reverse():
    """Verify reverse branch for 100% coverage."""
    # Triggers the 'if reverse:' branch (Line 42)
    res = sorted_array(5, reverse=True)
    assert res == [4, 3, 2, 1, 0]

def test_sorted_array_explicit_reverse():
    from arprax.algos.utils import sorted_array
    # We must save to a variable and check an element to ensure execution
    data = sorted_array(n=10, reverse=True)
    assert data[0] == 9 # This forces Line 42 to execute

def test_sorted_array_reverse_branch():
    from arprax.algos.utils import sorted_array
    # Explicitly call the parent function with the reverse flag
    res = sorted_array(5, reverse=True)
    assert res == [4, 3, 2, 1, 0]

def test_legacy_reverse_sorted_array():
    from arprax.algos.utils import reverse_sorted_array
    # This directly hits Line 42
    assert reverse_sorted_array(3) == [2, 1, 0]