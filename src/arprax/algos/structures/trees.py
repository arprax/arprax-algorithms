"""
Binary Search Tree (BST) Implementation.

This module provides a recursive implementation of a symbol table (map)
using a binary search tree. It supports efficient key-value lookups,
insertions, and ordered operations.

Features:
    - Generic Key-Value storage (Keys must be comparable).
    - Ordered iteration (In-order traversal).
    - Hibbard Deletion for efficient removal.
    - Rank and Select operations.

Time Complexity:
    - Average Case: O(log N) for search/insert/delete.
    - Worst Case: O(N) if the tree becomes unbalanced (sorted input).
      (Use Red-Black BST to guarantee O(log N)).

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Section 3.2.
"""

from typing import Any, Optional, List


class _Node:
    """
    Internal private class representing a node in the BST.
    """

    def __init__(self, key: Any, val: Any, size: int):
        self.key = key
        self.val = val
        self.left: Optional["_Node"] = None
        self.right: Optional["_Node"] = None
        self.size = size  # Number of nodes in subtree rooted here


class BinarySearchTree:
    """
    A symbol table implemented using a Binary Search Tree.
    Keys are kept in sorted order.
    """

    def __init__(self):
        """Initializes an empty binary search tree."""
        self._root: Optional[_Node] = None

    def size(self) -> int:
        """Returns the number of key-value pairs in the table."""
        return self._size(self._root)

    def _size(self, x: Optional[_Node]) -> int:
        if x is None:
            return 0
        return x.size

    def is_empty(self) -> bool:
        """Returns True if the table is empty."""
        return self.size() == 0

    def get(self, key: Any) -> Optional[Any]:
        """
        Returns the value associated with the given key.

        Args:
            key: The key to search for.

        Returns:
            The value associated with the key, or None if not found.
        """
        return self._get(self._root, key)

    def _get(self, x: Optional[_Node], key: Any) -> Optional[Any]:
        if x is None:
            return None

        # Assume keys are comparable
        if key < x.key:
            return self._get(x.left, key)
        elif key > x.key:
            return self._get(x.right, key)
        else:
            return x.val

    def contains(self, key: Any) -> bool:
        """Returns True if the table contains the given key."""
        return self.get(key) is not None

    def put(self, key: Any, val: Any) -> None:
        """
        Inserts the key-value pair into the table.
        If the key already exists, updates the value.
        If the value is None, deletes the key.

        Args:
            key: The key to insert.
            val: The value to associate.
        """
        if val is None:
            self.delete(key)
            return
        self._root = self._put(self._root, key, val)

    def _put(self, x: Optional[_Node], key: Any, val: Any) -> _Node:
        if x is None:
            return _Node(key, val, 1)

        if key < x.key:
            x.left = self._put(x.left, key, val)
        elif key > x.key:
            x.right = self._put(x.right, key, val)
        else:
            x.val = val

        x.size = 1 + self._size(x.left) + self._size(x.right)
        return x

    def min(self) -> Any:
        """Returns the smallest key in the table."""
        if self.is_empty():
            raise ValueError("Calls min() with empty symbol table")
        return self._min(self._root).key

    def _min(self, x: _Node) -> _Node:
        if x.left is None:
            return x
        return self._min(x.left)

    def max(self) -> Any:
        """Returns the largest key in the table."""
        if self.is_empty():
            raise ValueError("Calls max() with empty symbol table")
        return self._max(self._root).key

    def _max(self, x: _Node) -> _Node:
        if x.right is None:
            return x
        return self._max(x.right)

    def floor(self, key: Any) -> Optional[Any]:
        """
        Returns the largest key less than or equal to key.

        Args:
            key: The target key.

        Returns:
            The floor key, or None if no such key exists.
        """
        if self.is_empty():
            return None
        x = self._floor(self._root, key)
        if x is None:
            return None
        return x.key

    def _floor(self, x: Optional[_Node], key: Any) -> Optional[_Node]:
        if x is None:
            return None

        if key == x.key:
            return x
        if key < x.key:
            return self._floor(x.left, key)

        t = self._floor(x.right, key)
        if t is not None:
            return t
        return x

    def delete_min(self) -> None:
        """Removes the smallest key and associated value."""
        if self.is_empty():
            raise ValueError("Symbol table underflow")
        self._root = self._delete_min(self._root)

    def _delete_min(self, x: _Node) -> Optional[_Node]:
        if x.left is None:
            return x.right
        x.left = self._delete_min(x.left)
        x.size = 1 + self._size(x.left) + self._size(x.right)
        return x

    def delete(self, key: Any) -> None:
        """
        Removes the key and its value from the table.
        This uses Hibbard Deletion.
        """
        if not self.contains(key):
            return
        self._root = self._delete(self._root, key)

    def _delete(self, x: _Node, key: Any) -> Optional[_Node]:
        if x is None:
            return None

        if key < x.key:
            x.left = self._delete(x.left, key)
        elif key > x.key:
            x.right = self._delete(x.right, key)
        else:
            # Matches key, delete x
            if x.right is None:
                return x.left
            if x.left is None:
                return x.right

            # Case 3: Node has two children
            # Replace with successor (min of right subtree)
            t = x
            x = self._min(t.right)
            x.right = self._delete_min(t.right)
            x.left = t.left

        x.size = 1 + self._size(x.left) + self._size(x.right)
        return x

    def keys(self) -> List[Any]:
        """Returns all keys in the table in sorted order."""
        result: List[Any] = []
        self._keys(self._root, result)
        return result

    def _keys(self, x: Optional[_Node], result: List[Any]) -> None:
        if x is None:
            return
        self._keys(x.left, result)
        result.append(x.key)
        self._keys(x.right, result)


# --- Red-Black BST Implementation ---


class _RBNode:
    """Internal node for Red-Black BST."""

    RED = True
    BLACK = False

    def __init__(self, key: Any, val: Any, color: bool):
        self.key = key
        self.val = val
        self.left: Optional["_RBNode"] = None
        self.right: Optional["_RBNode"] = None
        self.color = color  # Color of link from parent to this node
        self.size = 1


class RedBlackBST:
    """
    A Left-Leaning Red-Black BST.
    Guarantees O(log N) search and insert times even in worst case.
    """

    def __init__(self):
        self._root: Optional[_RBNode] = None

    def _is_red(self, x: Optional[_RBNode]) -> bool:
        if x is None:
            return False
        return x.color == _RBNode.RED

    def size(self) -> int:
        return self._size(self._root)

    def _size(self, x: Optional[_RBNode]) -> int:
        if x is None:
            return 0
        return x.size

    def get(self, key: Any) -> Optional[Any]:
        """Standard BST search (identical to BST)."""
        return self._get(self._root, key)

    def _get(self, x: Optional[_RBNode], key: Any) -> Optional[Any]:
        while x is not None:
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                return x.val
        return None

    def put(self, key: Any, val: Any) -> None:
        """Inserts key-value pair, maintaining perfect black balance."""
        self._root = self._put(self._root, key, val)
        self._root.color = _RBNode.BLACK

    def _put(self, h: Optional[_RBNode], key: Any, val: Any) -> _RBNode:
        if h is None:
            return _RBNode(key, val, _RBNode.RED)

        if key < h.key:
            h.left = self._put(h.left, key, val)
        elif key > h.key:
            h.right = self._put(h.right, key, val)
        else:
            h.val = val

        # Fix-up right-leaning links
        if self._is_red(h.right) and not self._is_red(h.left):
            h = self._rotate_left(h)
        if self._is_red(h.left) and self._is_red(h.left.left):
            h = self._rotate_right(h)
        if self._is_red(h.left) and self._is_red(h.right):
            self._flip_colors(h)

        h.size = 1 + self._size(h.left) + self._size(h.right)
        return h

    # --- Helper Operations for Balancing ---

    def _rotate_left(self, h: _RBNode) -> _RBNode:
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = _RBNode.RED
        x.size = h.size
        h.size = 1 + self._size(h.left) + self._size(h.right)
        return x

    def _rotate_right(self, h: _RBNode) -> _RBNode:
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = _RBNode.RED
        x.size = h.size
        h.size = 1 + self._size(h.left) + self._size(h.right)
        return x

    def _flip_colors(self, h: _RBNode) -> None:
        h.color = not h.color
        if h.left:
            h.left.color = not h.left.color
        if h.right:
            h.right.color = not h.right.color
