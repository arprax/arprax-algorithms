import pytest
from arprax.algos.structures.disjoint import DisjointSet


def test_initialization():
    """Test that the structure initializes correctly."""
    ds = DisjointSet(10)
    assert ds.count == 10
    # Initially, every node is its own parent
    for i in range(10):
        assert ds.find(i) == i
        assert ds._size[i] == 1


def test_union_and_find():
    """Test basic union and connectivity."""
    ds = DisjointSet(10)

    # Union 0-1
    ds.union(0, 1)
    assert ds.connected(0, 1)
    assert ds.count == 9

    # Union 2-3 and 4-5
    ds.union(2, 3)
    ds.union(4, 5)
    assert ds.count == 7

    # Connect components: 0-1 with 2-3 -> {0,1,2,3}
    ds.union(1, 3)
    assert ds.connected(0, 2)
    assert ds.connected(0, 3)
    assert not ds.connected(0, 4)
    assert ds.count == 6


def test_redundant_union():
    """Test that unioning connected elements does nothing."""
    ds = DisjointSet(5)
    ds.union(0, 1)
    initial_count = ds.count

    # Union again should not change anything
    ds.union(0, 1)
    assert ds.count == initial_count


def test_path_compression_logic():
    """
    Test that finding an element compresses the path.
    We create a chain manually to force a deep tree, then find() to flatten it.
    """
    ds = DisjointSet(5)
    # Manually link 0->1->2->3->4 (Worst case without weighting)
    # We use internal variables to force a specific structure for testing
    ds._parent = [1, 2, 3, 4, 4]

    # Validate structure before compression
    # Parent of 0 is 1
    assert ds._parent[0] == 1

    # Operations
    root = ds.find(0)

    assert root == 4
    # After find(0), 0 should point directly to root (4) due to compression
    assert ds._parent[0] == 4
    # Intermediate nodes might also be compressed depending on implementation
    assert ds._parent[1] == 4


def test_invalid_indices():
    """Test error handling for out-of-bounds access."""
    ds = DisjointSet(5)

    with pytest.raises(IndexError):
        ds.find(10)

    with pytest.raises(IndexError):
        ds.find(-1)

    with pytest.raises(IndexError):
        ds.union(0, 10)


def test_invalid_init():
    """Test error handling for invalid initialization."""
    with pytest.raises(ValueError):
        DisjointSet(-5)


def test_weighted_union_behavior():
    """
    Test specifically that a smaller tree gets attached to a larger tree.
    This hits lines 135-136 in disjoint.py.
    """
    ds = DisjointSet(10)

    # 1. Create a "Large" tree of size 3 rooted at 0
    # Union 0-1, then 0-2.
    # Structure: 0 is parent of 1 and 2. Size of 0 is 3.
    ds.union(0, 1)
    ds.union(0, 2)

    root_large = ds.find(0)
    assert ds._size[root_large] == 3

    # 2. Create a "Small" tree of size 1 (just node 5)
    # Size of 5 is 1.
    root_small = ds.find(5)
    assert ds._size[root_small] == 1

    # 3. MERGE SMALL INTO LARGE (Trigger Lines 135-136)
    # We call union(small, large).
    # Logic: if size[small] < size[large]: attach small to large.
    ds.union(5, 0)

    # 4. Verify the merge happened correctly
    # The parent of 5 should now be 0 (or whatever 0's root is)
    assert ds.find(5) == ds.find(0)
    # The size of the large root should increase by 1
    assert ds._size[ds.find(0)] == 4
