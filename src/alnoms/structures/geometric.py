"""
Geometric Data Structures.

This module provides spatial partitioning structures for efficient geometric
searching, including Kd-Trees (2d-Trees) and Quadtrees.

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Section 3.6 / Chapter 6.
"""

from typing import Optional, Tuple


class KdTree:
    """
    A 2d-Tree implementation for 2D points.

    Uses alternating axis-aligned partitioning (vertical/horizontal) to
    organize points in 2D space.
    """

    class _Node:
        def __init__(self, point: Tuple[float, float], is_vertical: bool):
            self.point = point
            self.is_vertical = is_vertical
            self.left: Optional[KdTree._Node] = None
            self.right: Optional[KdTree._Node] = None

    def __init__(self):
        """Initializes an empty 2d-Tree."""
        self._root: Optional[KdTree._Node] = None
        self._size = 0

    def insert(self, point: Tuple[float, float]) -> None:
        """
        Inserts a point into the 2d-Tree.

        Args:
            point (Tuple[float, float]): The (x, y) coordinates to insert.
        """
        self._root = self._insert(self._root, point, True)

    def _insert(
        self, x: Optional[_Node], point: Tuple[float, float], is_vertical: bool
    ) -> _Node:
        if x is None:
            self._size += 1
            return self._Node(point, is_vertical)

        if point == x.point:
            return x

        # Compare based on orientation
        cmp = point[0] < x.point[0] if is_vertical else point[1] < x.point[1]

        if cmp:
            x.left = self._insert(x.left, point, not is_vertical)
        else:
            x.right = self._insert(x.right, point, not is_vertical)
        return x

    def contains(self, point: Tuple[float, float]) -> bool:
        """Checks if the tree contains the specified point."""
        return self._contains(self._root, point)

    def _contains(self, x: Optional[_Node], point: Tuple[float, float]) -> bool:
        if x is None:
            return False
        if x.point == point:
            return True

        cmp = point[0] < x.point[0] if x.is_vertical else point[1] < x.point[1]
        if cmp:
            return self._contains(x.left, point)
        else:
            return self._contains(x.right, point)

    def size(self) -> int:
        """Returns number of points in the tree."""
        return self._size


class Quadtree:
    """
    A Quadtree for 2D spatial partitioning.

    Partitions space into four quadrants (NW, NE, SW, SE).
    """

    class _Node:
        def __init__(self, x: float, y: float, value: Optional[any] = None):
            self.x = x
            self.y = y
            self.value = value
            self.nw = self.ne = self.sw = self.se = None

    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float):
        """
        Initializes a Quadtree within a specific bounding box.

        Args:
            x_min, y_min: Lower bounds of the area.
            x_max, y_max: Upper bounds of the area.
        """
        self._root: Optional[Quadtree._Node] = None
        self._bounds = (x_min, y_min, x_max, y_max)

    def insert(self, x: float, y: float, value: any) -> None:
        """Inserts a point with an associated value into the Quadtree."""
        self._root = self._insert(self._root, x, y, value)

    def _insert(self, h: Optional[_Node], x: float, y: float, value: any) -> _Node:
        if h is None:
            return self._Node(x, y, value)

        if x < h.x and y >= h.y:
            h.nw = self._insert(h.nw, x, y, value)
        elif x >= h.x and y >= h.y:
            h.ne = self._insert(h.ne, x, y, value)
        elif x < h.x and y < h.y:
            h.sw = self._insert(h.sw, x, y, value)
        else:
            h.se = self._insert(h.se, x, y, value)
        return h

    def query(self, x: float, y: float) -> Optional[any]:
        """Retrieves the value at exactly (x, y) if it exists."""
        return self._query(self._root, x, y)

    def _query(self, h: Optional[_Node], x: float, y: float) -> Optional[any]:
        if h is None:
            return None
        if h.x == x and h.y == y:
            return h.value

        if x < h.x and y >= h.y:
            return self._query(h.nw, x, y)
        elif x >= h.x and y >= h.y:
            return self._query(h.ne, x, y)
        elif x < h.x and y < h.y:
            return self._query(h.sw, x, y)
        else:
            return self._query(h.se, x, y)
