import pytest
from arprax.algos.structures.trees import BinarySearchTree, RedBlackBST, _RBNode


# --- SECTION 1: Standard Binary Search Tree (BST) Tests ---


def test_bst_basic_ops():
    """Verifies put, get, contains, and updates."""
    bst = BinarySearchTree()
    bst.put(10, "Original")
    bst.put(10, "Updated")  # Hits Line 130: updates existing value
    assert bst.get(10) == "Updated"
    assert bst.contains(10) is True
    assert bst.get(5) is None  # Hits Line 112: search miss (None)


def test_bst_put_none_deletes():
    """Hits Lines 101-102: val=None triggers delete."""
    bst = BinarySearchTree()
    bst.put("A", 1)
    bst.put("A", None)
    assert bst.get("A") is None
    assert bst.is_empty()


def test_bst_recursion_paths():
    """Covers recursive branches for get, size, and min/max."""
    bst = BinarySearchTree()
    # Inserting 10 -> 5 -> 2 forces two steps of left recursion for min
    # Inserting 20 forces right recursion for get/size
    for x in [10, 5, 2, 20]:
        bst.put(x, x)

    assert bst.get(20) == 20  # Hits Line 114: Recursive _get (right)
    assert bst.size() == 4  # Hits Line 134: _size recursion (right)
    assert bst.min() == 2  # Hits Line 152: _min recursion (left)
    assert bst.max() == 20


def test_bst_empty_exceptions():
    """Hits Lines 137-139, 155-156, and 163: Errors on empty tree."""
    bst = BinarySearchTree()
    with pytest.raises(ValueError, match="Calls max"):
        bst.max()
    with pytest.raises(ValueError, match="Calls min"):
        bst.min()
    with pytest.raises(ValueError, match="underflow"):
        bst.delete_min()
    assert bst.floor(10) is None


def test_bst_delete_min_logic():
    """Covers root deletion and recursive deletion of minimum."""
    bst = BinarySearchTree()
    # Case 1: Root is min (no left child)
    bst.put(10, 10)
    bst.put(20, 20)
    bst.delete_min()
    assert bst.min() == 20

    # Case 2: Recursion (min is deep left)
    bst.put(5, 5)
    bst.put(1, 1)
    bst.delete_min()
    assert bst.min() == 5


def test_bst_floor_logic():
    """Covers recursive floor searches in both branches."""
    bst = BinarySearchTree()
    # Structure: 10 (Root), 20 (Right), 15 (Right-Left)
    for x in [10, 20, 15]:
        bst.put(x, x)

    assert bst.floor(17) == 15  # Hits Line 176: Floor in right subtree
    assert bst.floor(9) is None


def test_bst_delete_branches():
    """Covers Hibbard deletion cases including nodes with 0, 1, or 2 children."""
    bst = BinarySearchTree()

    # 1. Delete Non-Existent
    bst.put(10, 10)
    bst.delete(99)
    assert bst.size() == 1

    # 2. Delete recursion (Left)
    bst.put(5, 5)
    bst.delete(5)  # Hits Line 196
    assert bst.size() == 1

    # 3. Delete node with ONLY Left child
    bst.put(20, 20)
    bst.put(15, 15)
    bst.delete(20)  # Hits Line 207: 20 has no right child
    assert bst.get(20) is None
    assert bst.get(15) == 15

    # 4. Delete node with TWO children (Successor Logic)
    # Build tree so 10 has 5 and 15 as children
    bst.put(10, 10)
    bst.put(5, 5)
    bst.put(15, 15)
    bst.put(12, 12)
    bst.delete(10)  # Hits Lines 210-214: Hibbard deletion
    assert bst.contains(10) is False


def test_bst_keys_traversal():
    """Verifies in-order traversal and empty state."""
    bst = BinarySearchTree()
    assert bst.keys() == []
    for x in [2, 1, 3]:
        bst.put(x, x)
    assert bst.keys() == [1, 2, 3]


# --- SECTION 2: Red-Black BST (LLRB) Tests ---


def test_rbt_basic_ops():
    """Verifies get, update, and search misses."""
    rb = RedBlackBST()
    rb.put("A", 1)
    rb.put("A", 2)  # Hits Line 298: update existing
    assert rb.get("A") == 2
    assert rb.get("Z") is None  # Hits Line 282: miss


def test_rbt_balancing_rotations():
    """Hits _rotate_left, _rotate_right, and _flip_colors via specific sequences."""
    # Sequence 1: rotate_left (Increasing order)
    rb = RedBlackBST()
    rb.put(1, "A")
    rb.put(2, "B")  # Hits rotate_left

    # Sequence 2: flip_colors (Balanced insertion)
    rb.put(3, "C")  # Hits flip_colors

    # Sequence 3: rotate_right (Decreasing order)
    rb.put(0, "D")  # Triggers rotate_right eventually via _put recursion

    assert rb.size() == 4
    assert rb.get(2) == "B"


def test_rb_color_flip_internal():
    """Surgically targets _flip_colors attribute guards and state changes."""
    rb = RedBlackBST()
    # Create a node and manually test partial branches for if h.left/h.right
    node = _RBNode(10, 10, False)

    # Path A: Children are None (Hits False branch of attribute guards)
    rb._flip_colors(node)
    assert node.color is True  # RED

    # Path B: Normal flip with children (Hits True branch of guards)
    node.left = _RBNode(5, 5, True)
    node.right = _RBNode(15, 15, True)
    rb._flip_colors(node)  # Flipped back to BLACK
    assert node.color is False
    assert node.left.color is False
