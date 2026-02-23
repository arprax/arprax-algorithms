from alnoms.structures.graphs import Graph, Digraph
from alnoms.algorithms.graph.traversal import (
    DepthFirstPaths,
    BreadthFirstPaths,
    Topological,
)


# --- DFS Tests ---


def test_dfs_paths():
    # 0-1, 0-2, 2-3
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(2, 3)

    dfs = DepthFirstPaths(g, 0)

    assert dfs.has_path_to(3)
    assert dfs.has_path_to(1)

    # Path to 3 should be 0-2-3 (DFS usually goes deep)
    # Note: Exact path depends on adjacency list order, but connectivity is invariant
    path = list(dfs.path_to(3))
    assert path[0] == 0
    assert path[-1] == 3
    assert 2 in path


def test_dfs_disconnected():
    g = Graph(3)
    g.add_edge(0, 1)
    # 2 is isolated

    dfs = DepthFirstPaths(g, 0)
    assert not dfs.has_path_to(2)
    assert dfs.path_to(2) is None


# --- BFS Tests ---


def test_bfs_shortest_path():
    # 0-1-2-3 (Length 3)
    # 0-3     (Length 1)
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(0, 3)  # Shortcut

    bfs = BreadthFirstPaths(g, 0)

    assert bfs.dist_to(3) == 1
    path = list(bfs.path_to(3))
    assert len(path) == 2  # [0, 3]


def test_bfs_dist():
    g = Graph(3)
    g.add_edge(0, 1)

    bfs = BreadthFirstPaths(g, 0)
    assert bfs.dist_to(0) == 0
    assert bfs.dist_to(1) == 1
    assert bfs.dist_to(2) == float("inf")


# --- Topological Sort Tests ---


def test_topological_sort():
    # 0 -> 1 -> 2
    # 0 -> 2
    dg = Digraph(3)
    dg.add_edge(0, 1)
    dg.add_edge(1, 2)
    dg.add_edge(0, 2)

    topo = Topological(dg)
    order = list(topo.order())

    # Valid order: [0, 1, 2]
    assert order.index(0) < order.index(1)
    assert order.index(1) < order.index(2)
    assert order.index(0) < order.index(2)


def test_topological_complex():
    # 0->5, 0->2, 3->5, 3->6 ... (Standard textbook DAG)
    # Simplified: 3->1->2
    dg = Digraph(4)
    dg.add_edge(3, 1)
    dg.add_edge(1, 2)
    # 0 is isolated

    topo = Topological(dg)
    order = list(topo.order())

    # 3 must come before 1, 1 before 2
    assert order.index(3) < order.index(1)
    assert order.index(1) < order.index(2)
