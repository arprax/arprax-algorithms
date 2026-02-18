"""
Network Flow Algorithms.

This module provides the Ford-Fulkerson algorithm for solving the max-flow
min-cut problem in flow networks.

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Section 6.4.
"""

from typing import List, Optional, Deque
from collections import deque
from arprax.algos.structures.graphs import FlowNetwork, FlowEdge


class FordFulkerson:
    """
    Computes the maximum flow and minimum cut in a flow network.

    This implementation uses the shortest augmenting path (Edmonds-Karp)
    approach via Breadth-First Search (BFS) to find paths in the residual
    graph, ensuring polynomial time complexity.
    """

    def __init__(self, G: FlowNetwork, s: int, t: int):
        """
        Initializes the solver and computes the maximum flow from s to t.

        Args:
            G (FlowNetwork): The flow network.
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

        # While an augmenting path exists in the residual graph
        while self._has_augmenting_path(G, s, t):
            # Compute bottleneck capacity of the path
            bottle = float("inf")
            v = t
            while v != s:
                edge = self._edge_to[v]
                bottle = min(bottle, edge.residual_capacity_to(v))
                v = edge.other(v)

            # Augment flow along the path
            v = t
            while v != s:
                self._edge_to[v].add_residual_flow_to(v, bottle)
                v = self._edge_to[v].other(v)

            self._value += bottle

    def _has_augmenting_path(self, G: FlowNetwork, s: int, t: int) -> bool:
        """
        Finds an augmenting path in the residual graph using BFS.

        Args:
            G (FlowNetwork): The flow network.
            s (int): The source vertex.
            t (int): The sink vertex.

        Returns:
            bool: True if an augmenting path exists, False otherwise.
        """
        self._edge_to = [None] * G.V()
        self._marked = [False] * G.V()

        queue: Deque[int] = deque([s])
        self._marked[s] = True

        while queue and not self._marked[t]:
            v = queue.popleft()
            for e in G.adj(v):
                w = e.other(v)
                # If there is residual capacity to w, and w hasn't been visited
                if e.residual_capacity_to(w) > 0 and not self._marked[w]:
                    self._edge_to[w] = e
                    self._marked[w] = True
                    queue.append(w)

        return self._marked[t]

    def value(self) -> float:
        """
        Returns the value of the maximum flow.

        Returns:
            float: Total flow from source to sink.
        """
        return self._value

    def in_cut(self, v: int) -> bool:
        """
        Returns true if vertex v is on the source side of the minimum cut.

        A vertex is in the min-cut if it is reachable from the source in
        the residual graph after the max-flow has been computed.

        Args:
            v (int): The vertex to check.

        Returns:
            bool: True if v is in the source-side of the min-cut.
        """
        return self._marked[v]
