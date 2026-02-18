"""
Arprax Algorithms: Sorting Module
Provides industrial-grade implementations of Selection, Bubble, and Merge Sort.
Each algorithm supports a 'visualize' flag to yield state snapshots for animation.
"""

from typing import List, Generator, Union


def selection_sort(
    arr: List[int], visualize: bool = False
) -> Union[List[int], Generator[List[int], None, None]]:
    """
    Implementation of Selection Sort.

    Iterates through the list to find the minimum element and places it at
    the current boundary of the sorted portion.

    Complexity:
        Time: O(N^2)
        Space: O(1) (In-place)

    Args:
        arr (List[int]): The list of integers to sort.
        visualize (bool): If True, returns a generator yielding snapshots of the array.

    Returns:
        Union[List[int], Generator]: The sorted list or a generator of intermediate states.
    """
    n = len(arr)
    data = list(arr)

    def generator():
        """Yields snapshots of the array for the Arprax Lab visualizer."""
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if data[j] < data[min_idx]:
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]
            yield list(data)

    if visualize:
        return generator()

    # Standard logic for non-visualized return
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    return data


def bubble_sort(
    arr: List[int], visualize: bool = False
) -> Union[List[int], Generator[List[int], None, None]]:
    """
    Implementation of Bubble Sort with early-exit optimization.

    Repeatedly steps through the list, compares adjacent elements, and swaps
    them if they are in the wrong order.

    Complexity:
        Time: O(N^2) (Worst/Average), O(N) (Best Case with early exit)
        Space: O(1) (In-place)

    Args:
        arr (List[int]): The list of integers to sort.
        visualize (bool): If True, returns a generator yielding snapshots of the array.

    Returns:
        Union[List[int], Generator]: The sorted list or a generator of intermediate states.
    """
    n = len(arr)
    data = list(arr)

    def generator():
        """Yields snapshots of the array for the Arprax Lab visualizer."""
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    swapped = True
                yield list(data)
            if not swapped:
                break

    if visualize:
        return generator()

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
        if not swapped:
            break
    return data


def merge_sort(
    arr: List[int], visualize: bool = False
) -> Union[List[int], Generator[List[int], None, None]]:
    """
    Implementation of Merge Sort.

    A divide-and-conquer algorithm that recursively splits the list in half
    and merges the sorted sub-lists.

    Complexity:
        Time: O(N log N)
        Space: O(N)

    Args:
        arr (List[int]): The list of integers to sort.
        visualize (bool): If True, returns a generator yielding snapshots of the array.

    Returns:
        Union[List[int], Generator]: The sorted list or a generator of intermediate states.
    """
    data = list(arr)

    def generator(left: int, right: int):
        """Yields snapshots of the array for the Arprax Lab visualizer."""
        if left < right:
            mid = (left + right) // 2
            yield from generator(left, mid)
            yield from generator(mid + 1, right)

            # Merge logic for visualization
            # Using descriptive names prevents the E741 Ruff error
            left_part, right_part = data[left : mid + 1], data[mid + 1 : right + 1]
            i = j = 0
            for k in range(left, right + 1):
                if i < len(left_part) and (
                    j >= len(right_part) or left_part[i] <= right_part[j]
                ):
                    data[k] = left_part[i]
                    i += 1
                else:
                    data[k] = right_part[j]
                    j += 1
                yield list(data)

    if visualize:
        return generator(0, len(data) - 1)

    # Standard recursive sort logic
    def sort(a: List[int]) -> List[int]:
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        L, R = sort(a[:mid]), sort(a[mid:])
        res, i, j = [], 0, 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                res.append(L[i])
                i += 1
            else:
                res.append(R[j])
                j += 1
        res.extend(L[i:])
        res.extend(R[j:])
        return res

    return sort(data)
