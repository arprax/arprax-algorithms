import pytest
from arprax.algos.algorithms.graph.shortest_path import (
    DirectedEdge,
    EdgeWeightedDigraph,
    DijkstraSP,
    BellmanFordSP,
)


# --- Graph Construction Tests ---


def test_directed_edge():
    e = DirectedEdge(0, 1, 0.5)
    assert e.from_vertex() == 0
    assert e.to_vertex() == 1
    assert e.weight == 0.5
    assert "0->1 0.50" in str(e)


def test_digraph_api():
    g = EdgeWeightedDigraph(3)
    e1 = DirectedEdge(0, 1, 0.5)
    e2 = DirectedEdge(1, 2, 0.5)
    g.add_edge(e1)
    g.add_edge(e2)

    assert g.E() == 2
    assert e1 in list(g.adj(0))


def test_digraph_validation():
    with pytest.raises(ValueError):
        EdgeWeightedDigraph(-1)
    g = EdgeWeightedDigraph(2)
    with pytest.raises(IndexError):
        g.add_edge(DirectedEdge(0, 5, 0.0))


# --- Dijkstra Tests ---


def test_dijkstra_basic():
    # 0 -> 1 (1.0)
    # 1 -> 2 (2.0)
    # 0 -> 2 (10.0) [Shortcut but heavier]
    g = EdgeWeightedDigraph(3)
    g.add_edge(DirectedEdge(0, 1, 1.0))
    g.add_edge(DirectedEdge(1, 2, 2.0))
    g.add_edge(DirectedEdge(0, 2, 10.0))

    sp = DijkstraSP(g, 0)

    assert sp.dist_to(2) == 3.0  # 1.0 + 2.0
    path = list(sp.path_to(2))
    assert len(path) == 2
    assert path[0].weight == 1.0
    assert path[1].weight == 2.0


def test_dijkstra_negative_weight_error():
    g = EdgeWeightedDigraph(2)
    g.add_edge(DirectedEdge(0, 1, -1.0))
    with pytest.raises(ValueError):
        DijkstraSP(g, 0)


def test_dijkstra_unreachable():
    g = EdgeWeightedDigraph(2)
    sp = DijkstraSP(g, 0)
    assert sp.dist_to(1) == float("inf")
    assert sp.path_to(1) is None


# --- Bellman-Ford Tests ---


def test_bellman_ford_basic():
    # 0 -> 1 (10.0)
    # 0 -> 2 (5.0)
    # 2 -> 1 (1.0)  -> Path 0-2-1 is cost 6.0
    g = EdgeWeightedDigraph(3)
    g.add_edge(DirectedEdge(0, 1, 10.0))
    g.add_edge(DirectedEdge(0, 2, 5.0))
    g.add_edge(DirectedEdge(2, 1, 1.0))

    sp = BellmanFordSP(g, 0)
    assert sp.dist_to(1) == 6.0
    assert sp.has_path_to(1)


def test_bellman_ford_negative_edges():
    # 0 -> 1 (5.0)
    # 1 -> 2 (-2.0) -> Total cost 3.0
    g = EdgeWeightedDigraph(3)
    g.add_edge(DirectedEdge(0, 1, 5.0))
    g.add_edge(DirectedEdge(1, 2, -2.0))

    sp = BellmanFordSP(g, 0)
    assert sp.dist_to(2) == 3.0
