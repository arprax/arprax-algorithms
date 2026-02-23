"""
Minimum Spanning Tree (MST) Algorithms.

This module provides algorithms to find the MST of an edge-weighted graph.
The MST is a subgraph that connects all vertices with the minimum possible
total edge weight and no cycles.

Classes:
    - KruskalMST: Uses a Disjoint Set (Union-Find) to build the MST by merging
      sorted edges. efficient for sparse graphs.
    - LazyPrimMST: Uses a Priority Queue to grow the MST from a starting vertex.

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Section 4.3.
"""

from typing import List, Iterable
import heapq
from alnoms.structures.graphs import EdgeWeightedGraph, Edge
from alnoms.structures.disjoint import DisjointSet


class KruskalMST:
    """
    Computes the Minimum Spanning Tree using Kruskal's Algorithm.

    Logic:
    1. Sort all edges by weight.
    2. Add the smallest edge to the MST unless it creates a cycle.
    3. Use Union-Find (DisjointSet) to detect cycles efficiently.

    Time Complexity: O(E log E)
    Space Complexity: O(E)
    """

    def __init__(self, G: EdgeWeightedGraph):
        """
        Computes the MST.

        Args:
            G (EdgeWeightedGraph): The graph to process.
        """
        self._mst: List[Edge] = []
        self._weight: float = 0.0

        # 1. Get all edges and sort them (or heapify)
        # We sort efficiently using Python's Timsort (O(E log E))
        edges = sorted(list(G.edges()))

        # 2. Initialize Disjoint Set
        uf = DisjointSet(G.V())

        # 3. Iterate through sorted edges
        for e in edges:
            v = e.either()
            w = e.other(v)

            # If v and w are already connected, adding this edge would create a cycle
            if uf.connected(v, w):
                continue

            # No cycle -> Add edge to MST and merge components
            uf.union(v, w)
            self._mst.append(e)
            self._weight += e.weight

            # Optimization: Stop if we have V-1 edges (Spanning Tree property)
            if len(self._mst) >= G.V() - 1:
                break

    def edges(self) -> Iterable[Edge]:
        """Returns the edges in the MST."""
        return self._mst

    def weight(self) -> float:
        """Returns the total weight of the MST."""
        return self._weight


class LazyPrimMST:
    """
    Computes the Minimum Spanning Tree using the Lazy Prim's Algorithm.

    Logic:
    1. Start at vertex 0.
    2. Add all edges connected to 0 to a Priority Queue (PQ).
    3. Extract the minimum edge from PQ.
    4. If the edge connects to a vertex not yet in the MST, add it.
    5. Repeat until the MST is complete.

    "Lazy" means we leave obsolete edges in the PQ and ignore them later
    (when we pop them and realize both endpoints are already visited).

    Time Complexity: O(E log E)
    Space Complexity: O(E)
    """

    def __init__(self, G: EdgeWeightedGraph):
        self._mst: List[Edge] = []
        self._weight: float = 0.0
        self._marked = [False] * G.V()
        self._pq: List[Edge] = []  # Min-heap of Edges

        # Assumption: Graph is connected. If not, this finds MST of component 0.
        # To handle disconnected graphs, we would loop over all vertices.
        if G.V() > 0:
            self._visit(G, 0)

        while self._pq:
            # Get lowest-weight edge from PQ
            e = heapq.heappop(self._pq)
            v = e.either()
            w = e.other(v)

            # Ignore if both endpoints are already in MST (Obsolete edge)
            if self._marked[v] and self._marked[w]:
                continue

            # Add edge to MST
            self._mst.append(e)
            self._weight += e.weight

            # Visit the vertex that wasn't in the tree yet
            if not self._marked[v]:
                self._visit(G, v)
            if not self._marked[w]:
                self._visit(G, w)

    def _visit(self, G: EdgeWeightedGraph, v: int) -> None:
        """Marks v and adds all valid edges from v to the PQ."""
        self._marked[v] = True
        for e in G.adj(v):
            if not self._marked[e.other(v)]:
                heapq.heappush(self._pq, e)

    def edges(self) -> Iterable[Edge]:
        return self._mst

    def weight(self) -> float:
        return self._weight
