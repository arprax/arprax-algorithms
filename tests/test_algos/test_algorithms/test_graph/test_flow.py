import pytest
from arprax.algos.structures.graphs import FlowNetwork, FlowEdge
from arprax.algos.algorithms.graph.flow import FordFulkerson


def test_ford_fulkerson_basic_flow():
    """
    Test a standard flow network to verify max flow value.
    Updated to reflect correct capacity of 3.0.
    """
    fn = FlowNetwork(4)
    # Source: 0, Sink: 3
    fn.add_edge(FlowEdge(0, 1, 2.0))
    fn.add_edge(FlowEdge(0, 2, 1.0))
    fn.add_edge(FlowEdge(1, 2, 1.0))
    fn.add_edge(FlowEdge(1, 3, 1.0))
    fn.add_edge(FlowEdge(2, 3, 2.0))

    ff = FordFulkerson(fn, 0, 3)

    # Corrected expectation:
    # Path 0-1-3 takes 1.0
    # Path 0-2-3 takes 1.0
    # Path 0-1-2-3 takes 1.0
    assert pytest.approx(ff.value()) == 3.0


def test_ford_fulkerson_min_cut_membership():
    """
    Verify that the min-cut reachable nodes are correctly marked.
    In a saturated network, nodes reachable in the residual graph are 'in_cut'.
    """
    fn = FlowNetwork(2)
    fn.add_edge(FlowEdge(0, 1, 5.0))

    ff = FordFulkerson(fn, 0, 1)

    assert ff.value() == 5.0
    # Source is always in the cut
    assert ff.in_cut(0) is True
    # Sink is NOT in the cut because the edge is saturated
    assert ff.in_cut(1) is False


def test_ford_fulkerson_complex_network():
    """
    Test a larger network from Sedgewick Section 6.4.
    Ensures BFS correctly finds multiple augmenting paths.
    """
    fn = FlowNetwork(6)
    # Source 0, Sink 5
    fn.add_edge(FlowEdge(0, 1, 16))
    fn.add_edge(FlowEdge(0, 2, 13))
    fn.add_edge(FlowEdge(1, 2, 10))
    fn.add_edge(FlowEdge(1, 3, 12))
    fn.add_edge(FlowEdge(2, 1, 4))
    fn.add_edge(FlowEdge(2, 4, 14))
    fn.add_edge(FlowEdge(3, 2, 9))
    fn.add_edge(FlowEdge(3, 5, 20))
    fn.add_edge(FlowEdge(4, 3, 7))
    fn.add_edge(FlowEdge(4, 5, 4))

    ff = FordFulkerson(fn, 0, 5)
    assert pytest.approx(ff.value()) == 23.0


def test_ford_fulkerson_disconnected():
    """Test behavior when no path exists from s to t."""
    fn = FlowNetwork(3)
    fn.add_edge(FlowEdge(0, 1, 10.0))
    # No edge to 2

    ff = FordFulkerson(fn, 0, 2)
    assert ff.value() == 0.0
    assert ff.in_cut(0) is True
    assert ff.in_cut(2) is False


def test_ford_fulkerson_validation_errors():
    """Test all error branches for source/sink validation."""
    fn = FlowNetwork(5)

    # Out of bounds low
    with pytest.raises(ValueError, match="out of bounds"):
        FordFulkerson(fn, -1, 3)

    # Out of bounds high
    with pytest.raises(ValueError, match="out of bounds"):
        FordFulkerson(fn, 0, 5)

    # Same source and sink
    with pytest.raises(ValueError, match="must be distinct"):
        FordFulkerson(fn, 2, 2)


def test_ford_fulkerson_bottleneck_logic():
    """
    Ensures that the bottleneck capacity is correctly calculated
    along a multi-edge path.
    """
    fn = FlowNetwork(3)
    fn.add_edge(FlowEdge(0, 1, 100.0))
    fn.add_edge(FlowEdge(1, 2, 5.0))  # This is the bottleneck

    ff = FordFulkerson(fn, 0, 2)
    assert ff.value() == 5.0
