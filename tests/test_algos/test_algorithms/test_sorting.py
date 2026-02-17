from arprax.algos.algorithms import merge_sort, bubble_sort


def test_sorting_algorithms():
    sample = [3, 1, 4, 1, 5]
    expected = [1, 1, 3, 4, 5]

    assert merge_sort(sample) == expected
    assert bubble_sort(sample) == expected


def test_sorting_empty_and_single():
    assert merge_sort([]) == []
    assert merge_sort([1]) == [1]