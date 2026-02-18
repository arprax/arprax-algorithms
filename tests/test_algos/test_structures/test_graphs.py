import pytest
from arprax.algos.structures.graphs import Graph, Digraph, Edge, EdgeWeightedGraph


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
