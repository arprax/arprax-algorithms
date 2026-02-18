"""
Arprax Algorithms: Sorting Module.

Provides industrial-grade implementations of fundamental sorting algorithms.
Includes elementary sorts (Selection, Insertion, Shell) and advanced sorts
(Merge, Quick, Heap).

Features:
    - Generator Support: All functions support a 'visualize=True' flag to yield
      intermediate states for animation.
    - Optimization: Quick Sort uses 3-way partitioning (Dijkstra) for duplicate handling.
    - Efficiency: Merge Sort uses a single auxiliary array to reduce memory overhead.

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Chapter 2.
"""

from typing import List, Generator, Union, Any


# --- Elementary Sorts ---


def selection_sort(
    arr: List[Any], visualize: bool = False
) -> Union[List[Any], Generator]:
    """
    Selection Sort: Scans for the minimum item and swaps it into place.

    Complexity: Time O(N^2) | Space O(1)
    """
    data = list(arr)
    n = len(data)

    def _algo():
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if data[j] < data[min_idx]:
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]
            if visualize:
                yield list(data)
        if not visualize:
            yield list(data)

    gen = _algo()
    return gen if visualize else list(gen)[-1]


def insertion_sort(
    arr: List[Any], visualize: bool = False
) -> Union[List[Any], Generator]:
    """
    Insertion Sort: Builds the sort by moving elements one at a time.
    Excellent for partially sorted arrays or small subarrays.

    Complexity: Time O(N^2) (O(N) best case) | Space O(1)
    """
    data = list(arr)
    n = len(data)

    def _algo():
        for i in range(1, n):
            for j in range(i, 0, -1):
                if data[j] < data[j - 1]:
                    data[j], data[j - 1] = data[j - 1], data[j]
                    if visualize:
                        yield list(data)
                else:
                    break
        if not visualize:
            yield list(data)

    gen = _algo()
    return gen if visualize else list(gen)[-1]


def shell_sort(arr: List[Any], visualize: bool = False) -> Union[List[Any], Generator]:
    """
    Shell Sort: An optimized Insertion Sort using 'h-gaps'.
    Moves elements long distances to produce a partially sorted array,
    then finishes with standard insertion sort.

    Complexity: Time O(N^1.5) approx | Space O(1)
    """
    data = list(arr)
    n = len(data)

    def _algo():
        # 1. Compute max h-sequence (Knuth's: 1, 4, 13, 40...)
        h = 1
        while h < n // 3:
            h = 3 * h + 1

        # 2. Sort
        while h >= 1:
            for i in range(h, n):
                # Insertion sort with gap 'h'
                for j in range(i, h - 1, -1):
                    if data[j] < data[j - h]:
                        data[j], data[j - h] = data[j - h], data[j]
                        if visualize:
                            yield list(data)
                    else:
                        break
            h //= 3
        if not visualize:
            yield list(data)

    gen = _algo()
    return gen if visualize else list(gen)[-1]


# --- Advanced Sorts ---


def merge_sort(arr: List[Any], visualize: bool = False) -> Union[List[Any], Generator]:
    """
    Merge Sort: Recursive divide-and-conquer.
    Guarantees O(N log N) time, but requires O(N) auxiliary space.
    """
    data = list(arr)
    aux = list(arr)  # Auxiliary array for merging

    def _merge(lo: int, mid: int, hi: int):
        # Copy to aux
        for k in range(lo, hi + 1):
            aux[k] = data[k]

        i, j = lo, mid + 1
        for k in range(lo, hi + 1):
            if i > mid:
                data[k] = aux[j]
                j += 1
            elif j > hi:
                data[k] = aux[i]
                i += 1
            elif aux[j] < aux[i]:
                data[k] = aux[j]
                j += 1
            else:
                data[k] = aux[i]
                i += 1

            if visualize:
                yield list(data)

    def _sort(lo: int, hi: int):
        if hi <= lo:
            return
        mid = lo + (hi - lo) // 2
        yield from _sort(lo, mid)
        yield from _sort(mid + 1, hi)
        yield from _merge(lo, mid, hi)

    def _wrapper():
        yield from _sort(0, len(data) - 1)
        if not visualize:
            yield data

    gen = _wrapper()
    return gen if visualize else list(gen)[-1]


def quick_sort(arr: List[Any], visualize: bool = False) -> Union[List[Any], Generator]:
    """
    Quick Sort (3-Way Partition): The standard for general purpose sorting.
    Uses Dijkstra's 3-way partitioning to handle duplicate keys efficiently.

    Complexity: Time O(N log N) average | Space O(log N) recursion
    """
    data = list(arr)

    def _sort(lo: int, hi: int):
        if hi <= lo:
            return

        # 3-Way Partitioning (lt, i, gt)
        lt, i, gt = lo, lo + 1, hi
        v = data[lo]

        while i <= gt:
            if data[i] < v:
                data[lt], data[i] = data[i], data[lt]
                lt += 1
                i += 1
                if visualize:
                    yield list(data)
            elif data[i] > v:
                data[i], data[gt] = data[gt], data[i]
                gt -= 1
                if visualize:
                    yield list(data)
            else:
                i += 1

        # Recurse
        yield from _sort(lo, lt - 1)
        yield from _sort(gt + 1, hi)

    def _wrapper():
        yield from _sort(0, len(data) - 1)
        if not visualize:
            yield data

    gen = _wrapper()
    return gen if visualize else list(gen)[-1]


def heap_sort(arr: List[Any], visualize: bool = False) -> Union[List[Any], Generator]:
    """
    Heap Sort: Uses a binary heap to sort in-place.
    Guarantees O(N log N) time with O(1) space.
    """
    data = list(arr)
    n = len(data)

    def _sink(k: int, max_n: int):
        while 2 * k + 1 < max_n:
            j = 2 * k + 1
            if j < max_n - 1 and data[j] < data[j + 1]:
                j += 1
            if data[k] >= data[j]:
                break
            data[k], data[j] = data[j], data[k]
            k = j
            if visualize:
                yield list(data)

    def _algo():
        # 1. Heap Construction (Bottom-up)
        for k in range(n // 2 - 1, -1, -1):
            yield from _sink(k, n)

        # 2. Sort-down
        k = n - 1
        while k > 0:
            data[0], data[k] = data[k], data[0]
            if visualize:
                yield list(data)
            yield from _sink(0, k)
            k -= 1

        if not visualize:
            yield list(data)

    gen = _algo()
    return gen if visualize else list(gen)[-1]
