import pytest
from arprax.algos.structures.trees import BinarySearchTree, RedBlackBST


# --- SECTION 1: Standard BST Tests ---


def test_bst_put_none_deletes():
    """Hits Lines 101-102: 'if val is None: self.delete(key); return'"""
    bst = BinarySearchTree()
    bst.put("A", 1)
    # This specifically triggers the 'if val is None' block
    bst.put("A", None)
    assert bst.get("A") is None
    assert bst.is_empty()


def test_bst_get_recursion():
    """Hits Line 114: Recursive _get (going right)."""
    bst = BinarySearchTree()
    bst.put(10, 10)
    bst.put(20, 20)  # Right child
    # Forces _get to traverse right
    assert bst.get(20) == 20


def test_bst_size_recursion():
    """Hits Line 134: _size recursion on right child."""
    bst = BinarySearchTree()
    bst.put(10, 10)
    bst.put(20, 20)
    # Forces _size to check right child's size
    assert bst.size() == 2


def test_bst_empty_exceptions():
    """Hits Lines 137-139, 155-156: ValueError on empty tree operations."""
    bst = BinarySearchTree()
    with pytest.raises(ValueError):
        bst.max()  # Line 137-139
    with pytest.raises(ValueError):
        bst.min()  # Line 151 check
    with pytest.raises(ValueError):
        bst.delete_min()  # Line 163 (which was 155 in your previous run)


def test_bst_min_max_recursion():
    """Hits Lines 151-152: Recursion in _min."""
    bst = BinarySearchTree()
    # Deep left tree to force _min recursion (Line 152)
    bst.put(10, 10)
    bst.put(5, 5)
    bst.put(1, 1)
    assert bst.min() == 1


def test_bst_delete_min_logic():
    """Hits Lines 159-170: Full delete_min logic."""
    bst = BinarySearchTree()

    # Case 1: Root is min (no left child) -> Hits 166
    bst.put(10, 10)
    bst.put(20, 20)
    bst.delete_min()
    assert bst.min() == 20

    # Case 2: Recursion (min is deep left) -> Hits 168-170
    bst.put(5, 5)
    bst.put(1, 1)  # 1 is new min
    bst.delete_min()
    assert bst.min() == 5


def test_bst_floor_recursion():
    """Hits Line 176: Recursion in _floor (Right branch)."""
    bst = BinarySearchTree()
    # Structure: 10 (Root), 20 (Right), 15 (Right-Left)
    bst.put(10, 10)
    bst.put(20, 20)
    bst.put(15, 15)

    # We look for floor(17).
    # 1. 17 > 10 (Go Right)
    # 2. 17 < 20 (Go Left) -> Found 15
    # 3. Returns 15 up the stack (Line 176)
    assert bst.floor(17) == 15
    assert bst.floor(9) is None


def test_bst_delete_edge_cases():
    """Hits Lines 191, 196, 201, 207: Specific delete branches."""
    bst = BinarySearchTree()

    # 1. Delete Non-Existent (Line 191)
    bst.put(10, 10)
    bst.delete(99)  # Should return immediately
    assert bst.size() == 1

    # 2. Delete recursion (Lines 196)
    bst.put(5, 5)  # Left child
    bst.delete(5)  # Forces 'key < x.key' recursion
    assert bst.size() == 1

    # 3. Delete Node with ONLY Left Child (Line 207)
    # This is the tricky one. Node 20 must have left child 15, NO right child.
    bst.put(20, 20)
    bst.put(15, 15)
    bst.delete(20)  # 20 has left child 15, right is None.
    assert bst.get(20) is None
    assert bst.get(15) == 15


def test_bst_keys_traversal():
    """Hits Lines 221-230: keys() full traversal."""
    bst = BinarySearchTree()
    # Empty keys check (Line 221)
    assert bst.keys() == []

    # Full traversal (Lines 226-230)
    bst.put(2, 2)
    bst.put(1, 1)
    bst.put(3, 3)
    # Should return sorted list
    assert bst.keys() == [1, 2, 3]


# --- SECTION 2: Red-Black BST Tests ---


def test_rbt_not_found():
    """Hits Line 282: RedBlackBST.get returns None."""
    rb = RedBlackBST()
    rb.put(1, 1)
    assert rb.get(99) is None


def test_rbt_update_existing():
    """Hits Line 298: RedBlackBST.put updates existing value."""
    rb = RedBlackBST()
    rb.put("A", 1)
    # This hits the 'else' block in _put (Line 298)
    rb.put("A", 2)
    assert rb.get("A") == 2


def test_rbt_rotations():
    """Ensures Red-Black logic (lines 300+) is active."""
    rb = RedBlackBST()
    keys = list("SEARCHEXAMPLE")
    for k in keys:
        rb.put(k, 1)
    assert rb.size() == len(set(keys))
