"""
Searching Algorithms.

This module provides efficient algorithms for searching in lists.
It covers standard Binary Search for sorted arrays and the QuickSelect
algorithm for finding the k-th smallest element in unsorted arrays.

Functions:
    - binary_search: Returns the index of a key in a sorted list.
    - rank: Returns the number of elements strictly less than the key.
    - quick_select: Finds the k-th smallest element in O(N) time (on average).

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Section 1.1 and 2.3.
"""

from typing import List, Any
import random


def binary_search(a: List[Any], key: Any) -> int:
    """
    Searches for a key in a sorted list using Binary Search.

    Time Complexity: O(log N)
    Space Complexity: O(1)

    Args:
        a (List[Any]): A sorted list of comparable elements.
        key (Any): The element to search for.

    Returns:
        int: The index of the key if found, otherwise -1.
    """
    lo = 0
    hi = len(a) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if key < a[mid]:
            hi = mid - 1
        elif key > a[mid]:
            lo = mid + 1
        else:
            return mid
    return -1


def rank(a: List[Any], key: Any) -> int:
    """
    Returns the number of elements in the sorted list strictly less than key.

    This is effectively a Binary Search that returns the insertion point.
    If the key exists, it returns the index of the first occurrence.
    If the key does not exist, it returns the index where it would be inserted.

    Time Complexity: O(log N)

    Args:
        a (List[Any]): A sorted list.
        key (Any): The element to rank.

    Returns:
        int: The rank of the key (0 to N).
    """
    lo = 0
    hi = len(a) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if key < a[mid]:
            hi = mid - 1
        elif key > a[mid]:
            lo = mid + 1
        else:
            # Handle duplicates: scan left to find the first occurrence
            while mid > 0 and a[mid - 1] == key:
                mid -= 1
            return mid

    return lo


def quick_select(a: List[Any], k: int) -> Any:
    """
    Finds the k-th smallest element in an unsorted list.

    This uses the partitioning logic from QuickSort to locate the element
    at index 'k' if the array were sorted. It does NOT fully sort the array.

    Time Complexity: O(N) average, O(N^2) worst case (rare with shuffle).
    Space Complexity: O(1) (in-place).

    Args:
        a (List[Any]): An unsorted list.
        k (int): The rank to retrieve (0 = min, N-1 = max).

    Returns:
        Any: The k-th smallest element.

    Raises:
        ValueError: If k is out of bounds.
    """
    if k < 0 or k >= len(a):
        raise ValueError(f"Rank {k} is out of bounds for list of size {len(a)}")

    # Shuffle needed to guarantee O(N) performance probabilistic guarantee
    # We copy to avoid modifying the user's original list unexpectedly
    # (Standard library behavior)
    aux = list(a)
    random.shuffle(aux)

    lo = 0
    hi = len(aux) - 1

    while hi > lo:
        j = _partition(aux, lo, hi)
        if j == k:
            return aux[k]
        elif j > k:
            hi = j - 1
        else:
            lo = j + 1

    return aux[k]


def _partition(a: List[Any], lo: int, hi: int) -> int:
    """
    Partitions the subarray a[lo..hi] so that a[lo..j-1] <= a[j] <= a[j+1..hi].
    Returns the index j.
    """
    i = lo
    j = hi + 1
    v = a[lo]

    while True:
        # Scan right
        i += 1
        while i < hi and a[i] < v:
            i += 1

        # Scan left
        j -= 1
        while j > lo and v < a[j]:
            j -= 1

        if i >= j:
            break

        a[i], a[j] = a[j], a[i]

    a[lo], a[j] = a[j], a[lo]
    return j
