import pytest
from alnoms.structures.graphs import FlowNetwork, FlowEdge
from alnoms.algorithms.math.reductions import FordFulkerson, BipartiteMatching


# --- Section 1: Ford-Fulkerson (Max-Flow / Min-Cut) Tests ---


def test_ford_fulkerson_standard():
    """
    Test a standard flow network from Sedgewick Section 6.4.
    6 vertices, 8 edges.
    """
    fn = FlowNetwork(6)
    # Source is 0, Sink is 5
    fn.add_edge(FlowEdge(0, 1, 2.0))
    fn.add_edge(FlowEdge(0, 2, 3.0))
    fn.add_edge(FlowEdge(1, 3, 3.0))
    fn.add_edge(FlowEdge(1, 4, 1.0))
    fn.add_edge(FlowEdge(2, 3, 1.0))
    fn.add_edge(FlowEdge(2, 4, 1.0))
    fn.add_edge(FlowEdge(3, 5, 2.0))
    fn.add_edge(FlowEdge(4, 5, 3.0))

    ff = FordFulkerson(fn, 0, 5)

    # Max flow should be 4.0
    assert pytest.approx(ff.value()) == 4.0

    # Check Min-Cut (Source side)
    # Vertex 0 must be in cut, vertex 5 must not be
    assert ff.in_cut(0) is True
    assert ff.in_cut(5) is False


def test_ford_fulkerson_no_path():
    """Test max flow when source and sink are disconnected."""
    fn = FlowNetwork(3)
    fn.add_edge(FlowEdge(0, 1, 10.0))
    # No edge to vertex 2 (sink)

    ff = FordFulkerson(fn, 0, 2)
    assert ff.value() == 0.0
    assert ff.in_cut(0) is True
    assert ff.in_cut(2) is False


def test_ford_fulkerson_errors():
    """Test defensive checks for out of bounds or invalid source/sink."""
    fn = FlowNetwork(5)

    with pytest.raises(ValueError, match="out of bounds"):
        FordFulkerson(fn, -1, 4)

    with pytest.raises(ValueError, match="out of bounds"):
        FordFulkerson(fn, 0, 10)

    with pytest.raises(ValueError, match="must be distinct"):
        FordFulkerson(fn, 2, 2)


# --- Section 2: Bipartite Matching Tests ---


def test_bipartite_matching_simple():
    """
    Test a basic bipartite matching scenario.
    Set 1: {0, 1, 2}
    Set 2: {0, 1, 2}
    Edges: (0-0), (0-1), (1-0), (2-2)
    """
    # adj[i] lists neighbors in set 2 for vertex i in set 1
    adj = [
        [0, 1],  # 0 can match with 0 or 1
        [0],  # 1 can only match with 0
        [2],  # 2 can only match with 2
    ]

    bm = BipartiteMatching(adj, 3, 3)

    # Max matching: (1-0), (0-1), (2-2) -> Size 3
    assert bm.size() == 3


def test_bipartite_matching_limited():
    """Test matching where one vertex is a bottleneck."""
    adj = [[0], [0], [0]]
    # All three vertices in set 1 want vertex 0 in set 2.
    bm = BipartiteMatching(adj, 3, 1)
    assert bm.size() == 1


def test_bipartite_matching_empty():
    """Test matching with no edges."""
    adj = [[], [], []]
    bm = BipartiteMatching(adj, 3, 3)
    assert bm.size() == 0
