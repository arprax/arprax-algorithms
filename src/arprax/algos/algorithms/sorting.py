from typing import List


def merge_sort(arr: List[int]) -> List[int]:
    """
    Industrial O(N log N) Merge Sort implementation.

    Args:
        arr (List[int]): The list of integers to be sorted.

    Returns:
        List[int]: A new list containing the sorted elements.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    # Recursive splitting
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    """
    Helper function to merge two sorted lists.

    Args:
        left (List[int]): The left sorted sub-list.
        right (List[int]): The right sorted sub-list.

    Returns:
        List[int]: The combined and sorted list.
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def bubble_sort(arr: List[int]) -> List[int]:
    """
    Standard O(N^2) Bubble Sort for educational profiling.

    Args:
        arr (List[int]): The list of integers to be sorted.

    Returns:
        List[int]: A sorted copy of the input list.
    """
    n = len(arr)
    # Working on a copy to keep the function pure
    data = arr[:]
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data