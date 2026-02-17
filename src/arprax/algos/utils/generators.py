import random
from typing import List


def random_array(n: int, lo: int = 0, hi: int = 1000) -> List[int]:
    """
    Generates an array of n random integers.

    Args:
        n (int): The number of elements to generate.
        lo (int): The lower bound of the random range (inclusive).
        hi (int): The upper bound of the random range (inclusive).

    Returns:
        List[int]: A list of n random integers.
    """
    return [random.randint(lo, hi) for _ in range(n)]


def sorted_array(n: int, reverse: bool = False) -> List[int]:
    """
    Generates an array of n integers in sorted order.

    Args:
        n (int): The number of elements to generate.
        reverse (bool): If True, returns descending order (Worst Case).

    Returns:
        List[int]: A list containing integers from 0 to n-1 (or reversed).
    """
    arr = list(range(n))
    if reverse:  # This satisfies the 'Missing Line 46' in coverage
        arr.reverse()
    return arr


def reverse_sorted_array(n: int) -> List[int]:
    """
    Legacy wrapper for descending order.
    Frequently used for 'Worst Case' algorithm testing.
    """
    return sorted_array(n, reverse=True)

