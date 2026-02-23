import pytest
from alnoms.algorithms.graph.shortest_path import (
    DirectedEdge,
    EdgeWeightedDigraph,
    DijkstraSP,
    BellmanFordSP,
)


# --- Graph Construction & Validation ---


def test_directed_edge_properties():
    """Verifies DirectedEdge attributes and string conversion."""
    e = DirectedEdge(0, 1, 0.5)
    assert e.from_vertex() == 0
    assert e.to_vertex() == 1
    assert e.weight == 0.5
    assert "0->1 0.50" in str(e)


def test_digraph_api_and_edges():
    """Verifies EdgeWeightedDigraph edge tracking and adjacencies."""
    g = EdgeWeightedDigraph(3)
    e = DirectedEdge(0, 1, 0.5)
    g.add_edge(e)
    assert g.V() == 3
    assert g.E() == 1
    assert e in list(g.adj(0))
    assert e in list(g.edges())


def test_digraph_validation():
    """Covers vertex and graph initialization error handling."""
    with pytest.raises(ValueError):
        EdgeWeightedDigraph(-1)
    g = EdgeWeightedDigraph(2)
    with pytest.raises(IndexError):
        g.add_edge(DirectedEdge(0, 5, 0.0))
    with pytest.raises(IndexError):
        list(g.adj(5))


# --- Dijkstra Algorithms Tests ---


def test_dijkstra_logic():
    """Tests shortest path calculation and path reconstruction."""
    g = EdgeWeightedDigraph(3)
    g.add_edge(DirectedEdge(0, 1, 1.0))
    g.add_edge(DirectedEdge(1, 2, 2.0))
    g.add_edge(DirectedEdge(0, 2, 10.0))

    sp = DijkstraSP(g, 0)
    assert sp.dist_to(2) == 3.0
    assert sp.has_path_to(2) is True

    path = list(sp.path_to(2))
    assert len(path) == 2
    assert path[0].from_vertex() == 0
    assert path[-1].to_vertex() == 2


def test_dijkstra_heap_optimization():
    """Hits the 'if dist > self._dist_to[v]: continue' optimization branch."""
    g = EdgeWeightedDigraph(3)
    # 0 -> 1 is 10.0, but 0 -> 2 -> 1 is 2.0
    # Vertex 1 will be pushed to the heap twice.
    g.add_edge(DirectedEdge(0, 1, 10.0))
    g.add_edge(DirectedEdge(0, 2, 1.0))
    g.add_edge(DirectedEdge(2, 1, 1.0))

    sp = DijkstraSP(g, 0)
    assert sp.dist_to(1) == 2.0


def test_dijkstra_errors_and_unreachable():
    """Covers negative weight detection and unreachable path logic."""
    g = EdgeWeightedDigraph(2)
    g.add_edge(DirectedEdge(0, 1, -1.0))
    with pytest.raises(ValueError):
        DijkstraSP(g, 0)

    # Test unreachable
    g2 = EdgeWeightedDigraph(2)
    sp = DijkstraSP(g2, 0)
    assert sp.has_path_to(1) is False
    assert sp.path_to(1) is None


# --- Bellman-Ford Algorithms Tests ---


def test_bellman_ford_basic():
    """Tests standard Bellman-Ford functionality with negative weights."""
    g = EdgeWeightedDigraph(3)
    g.add_edge(DirectedEdge(0, 1, 5.0))
    g.add_edge(DirectedEdge(1, 2, -2.0))  # Negative edge

    sp = BellmanFordSP(g, 0)
    assert sp.dist_to(2) == 3.0
    assert sp.has_path_to(2) is True
    assert sp.has_negative_cycle() is False
    assert list(sp.path_to(2))[1].weight == -2.0


def test_bellman_ford_cycle_check_trigger():
    """Triggers the 'self._cost % G.V() == 0' cycle check branch."""
    V = 3
    g = EdgeWeightedDigraph(V)
    # Add edges to increment cost to reach a multiple of V
    g.add_edge(DirectedEdge(0, 1, 1.0))
    g.add_edge(DirectedEdge(1, 2, 1.0))
    g.add_edge(DirectedEdge(2, 0, 1.0))

    sp = BellmanFordSP(g, 0)
    assert sp.has_negative_cycle() is False


def test_bellman_ford_unreachable():
    """Verifies behavior for vertices with no path."""
    g = EdgeWeightedDigraph(2)
    sp = BellmanFordSP(g, 0)
    assert sp.has_path_to(1) is False
    assert sp.path_to(1) is None
