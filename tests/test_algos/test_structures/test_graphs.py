import pytest
from arprax.algos.structures.graphs import (
    Graph,
    Digraph,
    Edge,
    EdgeWeightedGraph,
    FlowEdge,
    FlowNetwork,
)


# --- SECTION 1: Undirected Graph Tests ---


def test_graph_api():
    """Test basic API: V(), E(), add_edge(), adj()."""
    g = Graph(V=5)
    assert g.V() == 5
    assert g.E() == 0

    # Add edge 0-1 (Success path)
    g.add_edge(0, 1)
    assert g.E() == 1
    assert 1 in g.adj(0)
    assert g.degree(0) == 1


def test_graph_validation_explicit():
    """
    Ensures _validate_vertex raises IndexError.
    """
    g = Graph(5)

    # Case 1: Invalid V (Negative)
    with pytest.raises(IndexError):
        g.add_edge(-1, 2)

    # Case 2: Invalid W (Out of bounds)
    with pytest.raises(IndexError):
        g.add_edge(2, 10)

    # Case 3: Invalid V in adj()
    with pytest.raises(IndexError):
        g.adj(10)


def test_graph_init_error():
    with pytest.raises(ValueError):
        Graph(-1)


def test_graph_repr():
    g = Graph(2)
    g.add_edge(0, 1)
    assert "2 vertices" in str(g)


# --- SECTION 2: Digraph Tests (Targeting Line 134) ---


def test_digraph_api():
    """Success paths."""
    dg = Digraph(3)
    dg.add_edge(0, 1)
    assert 1 in dg.adj(0)
    assert dg.out_degree(0) == 1
    assert dg.in_degree(1) == 1

    rev = dg.reverse()
    assert 0 in rev.adj(1)


def test_digraph_validation_explicit():
    """
    HITS LINE 134: Explicitly trigger IndexError in Digraph.
    """
    dg = Digraph(5)

    # 1. Invalid Source (v)
    with pytest.raises(IndexError):
        dg.add_edge(10, 0)

    # 2. Invalid Destination (w) - This likely hits Line 134
    with pytest.raises(IndexError):
        dg.add_edge(0, 10)

    # 3. Invalid Access
    with pytest.raises(IndexError):
        dg.adj(10)

    with pytest.raises(IndexError):
        dg.out_degree(99)

    with pytest.raises(IndexError):
        dg.in_degree(99)


def test_digraph_init_error():
    with pytest.raises(ValueError):
        Digraph(-1)


# --- SECTION 3: EdgeWeightedGraph Tests (Targeting Line 263) ---


def test_ewg_api():
    """Success paths."""
    ewg = EdgeWeightedGraph(3)
    e1 = Edge(0, 1, 0.5)
    e2 = Edge(1, 2, 0.7)

    ewg.add_edge(e1)
    ewg.add_edge(e2)

    assert ewg.E() == 2
    assert e1 in list(ewg.edges())
    assert e1 in list(ewg.adj(0))


def test_ewg_validation_explicit():
    """
    HITS LINE 263: Explicitly trigger IndexError in EdgeWeightedGraph.
    """
    ewg = EdgeWeightedGraph(5)

    # 1. Invalid V (Source side of edge)
    # Edge(-1, 2) has v=-1. This triggers the FIRST validation check.
    e_bad_v = Edge(-1, 2, 0.0)
    with pytest.raises(IndexError):
        ewg.add_edge(e_bad_v)

    # 2. Invalid W (Destination side of edge)
    # Edge(0, 10) has v=0 (valid), w=10 (invalid).
    # This triggers the SECOND validation check (likely Line 263).
    e_bad_w = Edge(0, 10, 0.0)
    with pytest.raises(IndexError):
        ewg.add_edge(e_bad_w)

    # 3. Invalid Access
    with pytest.raises(IndexError):
        ewg.adj(10)


def test_ewg_init_error():
    with pytest.raises(ValueError):
        EdgeWeightedGraph(-1)


# --- SECTION 4: Edge Logic (Safety Checks) ---


def test_edge_logic_complete():
    """Hits Edge.other() branches and __str__."""
    v, w = 0, 1
    e = Edge(v, w, 0.5)

    # Hit 'if vertex == v'
    assert e.other(v) == w

    # Hit 'elif vertex == w'
    assert e.other(w) == v

    # Hit 'else raise ValueError'
    with pytest.raises(ValueError):
        e.other(99)

    # Hit __str__
    assert "0-1 0.50" in str(e)

    # Hit __lt__
    e2 = Edge(1, 2, 0.9)
    assert e < e2


# --- Tests for FlowEdge ---


def test_flow_edge_basic():
    """Tests basic properties and initialization of FlowEdge."""
    e = FlowEdge(1, 2, 5.0)
    assert e.from_v() == 1
    assert e.to_w() == 2
    assert e.capacity == 5.0
    assert e.flow == 0.0
    assert str(e) == "1->2 0.0/5.0"


def test_flow_edge_invalid_capacity():
    """Tests that negative capacity raises ValueError."""
    with pytest.raises(ValueError, match="capacity must be non-negative"):
        FlowEdge(1, 2, -1.0)


def test_flow_edge_other_endpoint():
    """Tests the other() method and its error handling."""
    e = FlowEdge(1, 2, 5.0)
    assert e.other(1) == 2
    assert e.other(2) == 1
    with pytest.raises(ValueError, match="Illegal endpoint"):
        e.other(3)


def test_flow_edge_residual_logic():
    """Tests residual capacity and flow updates for forward and backward edges."""
    e = FlowEdge(1, 2, 10.0)

    # Initial state
    assert e.residual_capacity_to(2) == 10.0  # Forward
    assert e.residual_capacity_to(1) == 0.0  # Backward

    # Add flow forward
    e.add_residual_flow_to(2, 4.0)
    assert e.flow == 4.0
    assert e.residual_capacity_to(2) == 6.0
    assert e.residual_capacity_to(1) == 4.0

    # Remove flow (add residual flow backward)
    e.add_residual_flow_to(1, 1.0)
    assert e.flow == 3.0

    # Test illegal endpoint for residual methods
    with pytest.raises(ValueError, match="Illegal endpoint"):
        e.residual_capacity_to(3)
    with pytest.raises(ValueError, match="Illegal endpoint"):
        e.add_residual_flow_to(3, 1.0)


# --- Tests for FlowNetwork ---


def test_flow_network_initialization():
    """Tests FlowNetwork initialization and error handling."""
    fn = FlowNetwork(10)
    assert fn.V() == 10
    assert fn.E() == 0
    with pytest.raises(ValueError, match="non-negative"):
        FlowNetwork(-1)


def test_flow_network_add_and_adj():
    """Tests adding edges and retrieving adjacency lists."""
    fn = FlowNetwork(3)
    e = FlowEdge(0, 1, 5.0)
    fn.add_edge(e)

    assert fn.E() == 1
    # Edge should appear in adj list of both endpoints
    assert e in fn.adj(0)
    assert e in fn.adj(1)


def test_flow_network_edges_iterator():
    """Tests the edges() iterator and ensures no double-counting."""
    fn = FlowNetwork(3)
    e1 = FlowEdge(0, 1, 5.0)
    e2 = FlowEdge(1, 2, 10.0)
    fn.add_edge(e1)
    fn.add_edge(e2)

    all_edges = list(fn.edges())
    assert len(all_edges) == 2
    assert e1 in all_edges
    assert e2 in all_edges
