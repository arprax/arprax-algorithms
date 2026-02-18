"""
Reductions and Flow Network Algorithms.

This module provides implementations of the Ford-Fulkerson algorithm for computing
maximum flow and minimum cuts in flow networks, as well as reductions for
problems like Bipartite Matching.

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Section 6.4.
"""

from typing import List, Optional, Deque
from collections import deque
from arprax.algos.structures.graphs import FlowNetwork, FlowEdge


class FordFulkerson:
    """
    Computes the maximum flow and minimum cut in a flow network.

    Uses the shortest augmenting path (Edmonds-Karp) implementation to ensure
    polynomial time complexity.
    """

    def __init__(self, G: FlowNetwork, s: int, t: int):
        """
        Initializes the Ford-Fulkerson solver and computes max flow.

        Args:
            G (FlowNetwork): The flow network to analyze.
            s (int): The source vertex.
            t (int): The sink vertex.

        Raises:
            ValueError: If s or t are out of bounds or s == t.
        """
        if s < 0 or s >= G.V() or t < 0 or t >= G.V():
            raise ValueError("Source or sink vertex out of bounds")
        if s == t:
            raise ValueError("Source and sink must be distinct")

        self._value = 0.0
        self._edge_to: List[Optional[FlowEdge]] = [None] * G.V()
        self._marked: List[bool] = [False] * G.V()

        while self._has_augmenting_path(G, s, t):
            # Compute bottleneck capacity
            bottle = float("inf")
            v = t
            while v != s:
                edge = self._edge_to[v]
                bottle = min(bottle, edge.residual_capacity_to(v))
                v = edge.other(v)

            # Augment flow
            v = t
            while v != s:
                self._edge_to[v].add_residual_flow_to(v, bottle)
                v = self._edge_to[v].other(v)

            self._value += bottle

    def _has_augmenting_path(self, G: FlowNetwork, s: int, t: int) -> bool:
        """Finds an augmenting path using BFS."""
        self._edge_to = [None] * G.V()
        self._marked = [False] * G.V()

        queue: Deque[int] = deque([s])
        self._marked[s] = True

        while queue and not self._marked[t]:
            v = queue.popleft()
            for e in G.adj(v):
                w = e.other(v)
                if e.residual_capacity_to(w) > 0 and not self._marked[w]:
                    self._edge_to[w] = e
                    self._marked[w] = True
                    queue.append(w)

        return self._marked[t]

    def value(self) -> float:
        """Returns the value of the maximum flow."""
        return self._value

    def in_cut(self, v: int) -> bool:
        """
        Returns true if vertex v is on the source side of the minimum cut.

        Args:
            v (int): The vertex to check.
        """
        return self._marked[v]


class BipartiteMatching:
    """
    Solves the Maximum Bipartite Matching problem via reduction to Max-Flow.
    """

    def __init__(self, adj: List[List[int]], n: int, m: int):
        """
        Computes maximum matching in a bipartite graph.

        Args:
            adj (List[List[int]]): Adjacency list where adj[i] contains neighbors
                                   of vertex i in the first set.
            n (int): Number of vertices in the first set (0 to n-1).
            m (int): Number of vertices in the second set (0 to m-1).
        """
        # Create a flow network with n + m + 2 vertices
        # source = n + m, sink = n + m + 1
        source = n + m
        sink = n + m + 1
        fn = FlowNetwork(n + m + 2)

        # Edges from source to first set
        for i in range(n):
            fn.add_edge(FlowEdge(source, i, 1.0))

        # Edges between sets
        for i in range(n):
            for neighbor in adj[i]:
                fn.add_edge(FlowEdge(i, n + neighbor, 1.0))

        # Edges from second set to sink
        for j in range(m):
            fn.add_edge(FlowEdge(n + j, sink, 1.0))

        self._ff = FordFulkerson(fn, source, sink)
        self._matching_size = int(self._ff.value())

    def size(self) -> int:
        """Returns the maximum matching size."""
        return self._matching_size
