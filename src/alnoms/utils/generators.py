"""
Alnoms: Data Generators
Provides industrial-grade tools for creating research-ready datasets.
"""

import random
from typing import List


def random_array(n: int, lo: int = 0, hi: int = 1000) -> List[int]:
    """
    Generates an array of n random integers using Python's built-in random module.

    This serves as the default, dependency-free generator for the library.

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
    if reverse:
        arr.reverse()
    return arr


def reverse_sorted_array(n: int) -> List[int]:
    """
    Legacy wrapper for descending order.

    Frequently used for 'Worst Case' algorithm testing in the Arprax Lab.

    Args:
        n (int): The number of elements to generate.

    Returns:
        List[int]: A list containing integers from n-1 down to 0.
    """
    return sorted_array(n, reverse=True)


def large_scale_dataset(n: int) -> List[int]:
    """
    High-performance data generator for large-scale research.

    Attempts to use NumPy for speed if available; otherwise, falls back
    to standard Python random generation.

    Args:
        n (int): The number of elements to generate.

    Returns:
        List[int]: A list of random integers.
    """
    try:
        import numpy as np

        # NumPy is much faster for generating millions of integers
        return np.random.randint(0, 1000, n).tolist()  # pragma: no cover
    except ImportError:
        # Graceful fallback for the 'Ultra-Lean' configuration
        return random_array(n)
