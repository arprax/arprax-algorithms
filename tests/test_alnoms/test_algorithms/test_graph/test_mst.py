import pytest
from alnoms.structures.graphs import EdgeWeightedGraph, Edge
from alnoms.algorithms.graph.mst import KruskalMST, LazyPrimMST


def create_test_graph():
    """
    Creates a standard weighted graph.
    Vertices: 4
    Edges:
    0-1 (0.5)
    1-2 (0.4)
    2-3 (0.3)
    0-2 (0.8) - Heavy, should be skipped (creates cycle with 0-1-2)
    """
    g = EdgeWeightedGraph(4)
    g.add_edge(Edge(0, 1, 0.5))
    g.add_edge(Edge(1, 2, 0.4))
    g.add_edge(Edge(2, 3, 0.3))
    g.add_edge(Edge(0, 2, 0.8))  # Redundant edge
    return g


def test_kruskal_mst():
    g = create_test_graph()
    mst = KruskalMST(g)

    # Expected MST: 2-3(0.3), 1-2(0.4), 0-1(0.5)
    # Total Weight: 1.2
    assert pytest.approx(mst.weight()) == 1.2
    edges = list(mst.edges())
    assert len(edges) == 3

    # Verify the heavy edge (0.8) is NOT in the MST
    for e in edges:
        assert e.weight < 0.8


def test_prim_mst():
    g = create_test_graph()
    mst = LazyPrimMST(g)

    # Prim should find the exact same weight
    assert pytest.approx(mst.weight()) == 1.2
    assert len(list(mst.edges())) == 3


def test_mst_disconnected():
    """Test behavior on a disconnected graph (forest)."""
    # 0-1 (1.0)
    # 2-3 (2.0)
    g = EdgeWeightedGraph(4)
    g.add_edge(Edge(0, 1, 1.0))
    g.add_edge(Edge(2, 3, 2.0))

    # Kruskal handles forests natively (finds MST for all components)
    kruskal = KruskalMST(g)
    assert pytest.approx(kruskal.weight()) == 3.0
    assert len(list(kruskal.edges())) == 2

    # LazyPrim (as implemented) starts at 0 and finds MST for that component only.
    # If the requirement is a Minimum Spanning Forest, Prim needs an outer loop.
    # The current implementation visits component 0.
    prim = LazyPrimMST(g)
    assert pytest.approx(prim.weight()) == 1.0  # Only 0-1
    assert len(list(prim.edges())) == 1


def test_mst_single_vertex():
    g = EdgeWeightedGraph(1)
    mst = KruskalMST(g)
    assert mst.weight() == 0.0
    assert len(list(mst.edges())) == 0
