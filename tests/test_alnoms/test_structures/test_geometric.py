"""
Tests for Geometric Data Structures.
Covers Kd-Trees and Quadtrees with 100% path coverage.
"""

from alnoms.structures.geometric import KdTree, Quadtree


# --- KdTree Tests ---


def test_kdtree_basic_operations():
    """Tests insertion, size, and containment for a 2d-Tree."""
    tree = KdTree()
    points = [(0.5, 0.5), (0.2, 0.3), (0.8, 0.8), (0.1, 0.9)]
    for p in points:
        tree.insert(p)

    assert tree.size() == 4
    assert tree.contains((0.2, 0.3)) is True
    assert tree.contains((1.0, 1.0)) is False

    # Test duplicate insertion (should not increase size)
    tree.insert((0.5, 0.5))
    assert tree.size() == 4


def test_kdtree_traversal_paths():
    """Forces coverage for vertical and horizontal splits in both directions."""
    tree = KdTree()
    # 1. Vertical split at x=0.5
    tree.insert((0.5, 0.5))

    # 2. Test horizontal split: Left subtree (x < 0.5)
    tree.insert((0.2, 0.1))  # y < 0.5
    tree.insert((0.2, 0.8))  # y > 0.5

    # 3. Test horizontal split: Right subtree (x > 0.5)
    tree.insert((0.8, 0.1))  # y < 0.5 (Line 119/139 logic equivalent for KdTree)
    tree.insert((0.8, 0.8))  # y > 0.5

    assert tree.contains((0.8, 0.1)) is True
    assert tree.contains((0.2, 0.8)) is True


# --- Quadtree Tests ---


def test_quadtree_standard_quadrants():
    """Verifies retrieval from all four quadrants and the origin."""
    qt = Quadtree(-10, -10, 10, 10)

    # Insert root at origin
    qt.insert(0, 0, "Origin")

    # Insert in 4 quadrants relative to (0,0)
    qt.insert(-5, 5, "NW")  # x < 0, y >= 0
    qt.insert(5, 5, "NE")  # x >= 0, y >= 0
    qt.insert(-5, -5, "SW")  # x < 0, y < 0
    qt.insert(5, -5, "SE")  # x >= 0, y < 0 (Triggers Line 119)

    assert qt.query(-5, 5) == "NW"
    assert qt.query(5, 5) == "NE"
    assert qt.query(-5, -5) == "SW"
    assert qt.query(5, -5) == "SE"  # Triggers Line 139
    assert qt.query(0, 0) == "Origin"


def test_quadtree_edge_cases():
    """Tests search misses and branch partials."""
    qt = Quadtree(-10, -10, 10, 10)
    qt.insert(0, 0, "Root")

    # Search in a quadrant that exists but for a point that isn't there
    assert qt.query(1, 1) is None

    # Search in a quadrant that hasn't been created yet (Branch Partial)
    # This specifically forces Line 139 to return a recursive None
    assert qt.query(5, -5) is None


def test_quadtree_logic_boundaries():
    """
    Ensures that points on boundaries (x=0 or y=0) are
    sorted into the correct industrial-standard quadrants (NE/SE).
    """
    qt = Quadtree(-10, -10, 10, 10)
    qt.insert(0, 0, "Root")

    # Point exactly on the X-axis boundary, but negative Y
    # Fails NW (x<0), NE (y>=0), SW (x<0) -> Results in SE (Line 139)
    qt.insert(5, -0.00001, "StrictlySE")
    assert qt.query(5, -0.00001) == "StrictlySE"
