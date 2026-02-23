"""
Disjoint Set (Union-Find) Data Structure.

This module implements the Disjoint Set data structure, also known as Union-Find.
It models a collection of disjoint sets, supporting efficient 'union' (merge)
and 'find' (lookup) operations.

Implementation Details:
    - Algorithm: Weighted Quick-Union with Path Compression.
    - Time Complexity: O(alpha(N)) for both union and find, where alpha is the
      inverse Ackermann function. In practice, this is nearly constant time.
    - Space Complexity: O(N) linear space.

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Section 1.5.
"""

from typing import List


class DisjointSet:
    """
    A data structure to manage a set of elements partitioned into disjoint subsets.

    This implementation uses 'weighted quick-union by size' to minimize tree height
    and 'path compression' to flatten the tree during find operations.
    """

    def __init__(self, n: int):
        """
        Initializes an empty disjoint set structure with n elements (0 to n-1).

        Args:
            n (int): The number of elements. Must be non-negative.

        Raises:
            ValueError: If n is negative.
        """
        if n < 0:
            raise ValueError(f"Number of elements must be non-negative, got {n}")

        # count is the number of independent components
        self._count: int = n

        # parent[i] indicates the parent of node i
        # If parent[i] == i, then i is a root
        self._parent: List[int] = list(range(n))

        # size[i] indicates the size of the tree rooted at i
        # This is strictly used for the weighting optimization
        self._size: List[int] = [1] * n

    @property
    def count(self) -> int:
        """
        Returns the number of disjoint sets (connected components).

        Returns:
            int: The number of components.
        """
        return self._count

    def find(self, p: int) -> int:
        """
        Returns the canonical element (root) of the set containing element p.

        This method employs path compression: after finding the root, it links
        every visited node directly to the root, flattening the structure for
        future operations.

        Args:
            p (int): The element to look up.

        Returns:
            int: The canonical root identifier of the component.

        Raises:
            IndexError: If p is not a valid index (0 <= p < n).
        """
        self._validate(p)

        root = p
        # 1. Find the root
        while root != self._parent[root]:
            root = self._parent[root]

        # 2. Path Compression
        # Traverse the path again and point every node directly to the root
        while p != root:
            new_p = self._parent[p]
            self._parent[p] = root
            p = new_p

        return root

    def connected(self, p: int, q: int) -> bool:
        """
        Determines whether elements p and q are in the same set.

        Args:
            p (int): First element.
            q (int): Second element.

        Returns:
            bool: True if p and q are connected, False otherwise.

        Raises:
            IndexError: If p or q are invalid indices.
        """
        return self.find(p) == self.find(q)

    def union(self, p: int, q: int) -> None:
        """
        Merges the set containing element p with the set containing element q.

        If p and q are already in the same set, this method returns immediately.
        Otherwise, it merges the smaller tree into the larger tree (weighted union).

        Args:
            p (int): First element.
            q (int): Second element.

        Raises:
            IndexError: If p or q are invalid indices.
        """
        root_p = self.find(p)
        root_q = self.find(q)

        # Already connected, nothing to do
        if root_p == root_q:
            return

        # Weighted Union: Link smaller tree to larger tree
        if self._size[root_p] < self._size[root_q]:
            self._parent[root_p] = root_q
            self._size[root_q] += self._size[root_p]
        else:
            self._parent[root_q] = root_p
            self._size[root_p] += self._size[root_q]

        self._count -= 1

    def _validate(self, p: int) -> None:
        """
        Validates that p is a valid index.

        Args:
            p (int): The index to validate.

        Raises:
            IndexError: If index is out of bounds.
        """
        n = len(self._parent)
        if p < 0 or p >= n:
            raise IndexError(f"index {p} is not between 0 and {n - 1}")
