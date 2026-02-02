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


def sorted_array(n: int) -> List[int]:
    """
    Generates an array of n integers in ascending order.

    Args:
        n (int): The number of elements to generate.

    Returns:
        List[int]: A list containing integers from 0 to n-1.
    """
    return list(range(n))


def reverse_sorted_array(n: int) -> List[int]:
    """
    Generates an array of n integers in descending order.

    This is frequently used to test "Worst Case" scenarios for algorithms
    like QuickSort or BubbleSort.

    Args:
        n (int): The number of elements to generate.

    Returns:
        List[int]: A list containing integers from n down to 1.
    """
    return list(range(n, 0, -1))