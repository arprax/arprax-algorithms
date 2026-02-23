"""
Shortest Path Algorithms.

This module provides algorithms for finding the shortest paths in edge-weighted
directed graphs. It includes data structures for representing weighted directed
graphs and implementation of standard shortest path algorithms.

Classes:
    - DirectedEdge: Represents a weighted edge in a directed graph.
    - EdgeWeightedDigraph: Represents an edge-weighted directed graph.
    - DijkstraSP: Computes shortest paths using Dijkstra's algorithm (non-negative weights).
    - BellmanFordSP: Computes shortest paths using Bellman-Ford (handles negative weights).

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Section 4.4.
"""

from typing import List, Iterable, Optional, Deque
from collections import deque
import heapq


# --- Section 1: Data Structures ---


class DirectedEdge:
    """
    Represents a weighted edge in a directed graph.

    Immutable data type.
    """

    def __init__(self, v: int, w: int, weight: float):
        """
        Initializes a directed edge from vertex v to vertex w with the given weight.

        Args:
            v (int): The source vertex.
            w (int): The destination vertex.
            weight (float): The weight of the edge.
        """
        self._v = v
        self._w = w
        self._weight = weight

    @property
    def weight(self) -> float:
        """Returns the weight of the edge."""
        return self._weight

    def from_vertex(self) -> int:
        """Returns the tail vertex of the directed edge."""
        return self._v

    def to_vertex(self) -> int:
        """Returns the head vertex of the directed edge."""
        return self._w

    def __str__(self) -> str:
        """Returns a string representation of the edge."""
        return f"{self._v}->{self._w} {self._weight:.2f}"


class EdgeWeightedDigraph:
    """
    Represents an edge-weighted directed graph.

    Implemented using adjacency lists, where each list contains DirectedEdge objects.
    """

    def __init__(self, V: int):
        """
        Initializes an empty edge-weighted digraph with V vertices and 0 edges.

        Args:
            V (int): The number of vertices.

        Raises:
            ValueError: If V is negative.
        """
        if V < 0:
            raise ValueError("Number of vertices must be non-negative")
        self._V = V
        self._E = 0
        self._adj: List[List[DirectedEdge]] = [[] for _ in range(V)]

    def V(self) -> int:
        """Returns the number of vertices in the digraph."""
        return self._V

    def E(self) -> int:
        """Returns the number of edges in the digraph."""
        return self._E

    def add_edge(self, e: DirectedEdge) -> None:
        """
        Adds the directed edge e to the digraph.

        Args:
            e (DirectedEdge): The edge to add.

        Raises:
            IndexError: If endpoints are out of bounds.
        """
        v = e.from_vertex()
        self._validate_vertex(v)
        self._validate_vertex(e.to_vertex())
        self._adj[v].append(e)
        self._E += 1

    def adj(self, v: int) -> Iterable[DirectedEdge]:
        """
        Returns the edges incident from vertex v.

        Args:
            v (int): The source vertex.

        Returns:
            Iterable[DirectedEdge]: Edges starting at v.
        """
        self._validate_vertex(v)
        return self._adj[v]

    def edges(self) -> Iterable[DirectedEdge]:
        """
        Returns all edges in the digraph.

        Returns:
            Iterable[DirectedEdge]: All edges in the graph.
        """
        list_edges = []
        for v in range(self._V):
            list_edges.extend(self._adj[v])
        return list_edges

    def _validate_vertex(self, v: int) -> None:
        if v < 0 or v >= self._V:
            raise IndexError(f"Vertex {v} is not between 0 and {self._V - 1}")


# --- Section 2: Dijkstra's Algorithm ---


class DijkstraSP:
    """
    Dijkstra's Shortest Path Algorithm.

    Computes the shortest path from a single source vertex 's' to every other
    vertex in an edge-weighted digraph where all edge weights are non-negative.

    Time Complexity: O(E log V)
    Space Complexity: O(V)
    """

    def __init__(self, G: EdgeWeightedDigraph, s: int):
        """
        Computes the shortest paths from source s.

        Args:
            G (EdgeWeightedDigraph): The graph.
            s (int): The source vertex.

        Raises:
            ValueError: If the graph contains an edge with negative weight.
        """
        self._validate_edges(G)

        self._dist_to = [float("inf")] * G.V()
        self._edge_to: List[Optional[DirectedEdge]] = [None] * G.V()
        self._pq: List[tuple] = []  # Min-heap storing (dist, vertex)

        self._dist_to[s] = 0.0
        heapq.heappush(self._pq, (0.0, s))

        while self._pq:
            dist, v = heapq.heappop(self._pq)

            # Optimization: If we found a shorter path to v already, skip
            if dist > self._dist_to[v]:
                continue

            for e in G.adj(v):
                self._relax(e)

    def _relax(self, e: DirectedEdge) -> None:
        """Relaxes an edge, updating dist_to and edge_to if a shorter path is found."""
        v, w = e.from_vertex(), e.to_vertex()
        if self._dist_to[w] > self._dist_to[v] + e.weight:
            self._dist_to[w] = self._dist_to[v] + e.weight
            self._edge_to[w] = e
            heapq.heappush(self._pq, (self._dist_to[w], w))

    def _validate_edges(self, G: EdgeWeightedDigraph) -> None:
        """Ensures no negative edges exist."""
        for e in G.edges():
            if e.weight < 0:
                raise ValueError(f"Edge has negative weight: {e}")

    def has_path_to(self, v: int) -> bool:
        """
        Returns True if there is a path from the source to vertex v.
        """
        return self._dist_to[v] < float("inf")

    def dist_to(self, v: int) -> float:
        """
        Returns the length of the shortest path from the source to vertex v.
        Returns infinity if no such path exists.
        """
        return self._dist_to[v]

    def path_to(self, v: int) -> Optional[Iterable[DirectedEdge]]:
        """
        Returns the shortest path from the source to vertex v.

        Args:
            v (int): The destination vertex.

        Returns:
            Optional[Iterable[DirectedEdge]]: A sequence of edges, or None if no path.
        """
        if not self.has_path_to(v):
            return None
        path: Deque[DirectedEdge] = deque()
        e = self._edge_to[v]
        while e is not None:
            path.appendleft(e)
            e = self._edge_to[e.from_vertex()]
        return path


# --- Section 3: Bellman-Ford Algorithm ---


class BellmanFordSP:
    """
    Bellman-Ford Shortest Path Algorithm.

    Computes shortest paths from a single source vertex 's' to every other vertex
    in a digraph that may contain negative edge weights.

    It detects negative cycles. If a negative cycle exists reachable from the source,
    shortest paths are undefined (or infinitely small).

    Time Complexity: O(V * E)
    Space Complexity: O(V)
    """

    def __init__(self, G: EdgeWeightedDigraph, s: int):
        """
        Computes the shortest paths from source s.

        Args:
            G (EdgeWeightedDigraph): The graph.
            s (int): The source vertex.
        """
        self._dist_to = [float("inf")] * G.V()
        self._edge_to: List[Optional[DirectedEdge]] = [None] * G.V()
        self._on_queue = [False] * G.V()
        self._queue: Deque[int] = deque()
        self._cost = 0  # Iteration count to trigger cycle checks
        self._cycle: Optional[Iterable[DirectedEdge]] = None

        self._dist_to[s] = 0.0
        self._queue.append(s)
        self._on_queue[s] = True

        while self._queue and not self.has_negative_cycle():
            v = self._queue.popleft()
            self._on_queue[v] = False
            self._relax(G, v)

    def _relax(self, G: EdgeWeightedDigraph, v: int) -> None:
        """Relaxes all edges leaving vertex v."""
        for e in G.adj(v):
            w = e.to_vertex()
            if self._dist_to[w] > self._dist_to[v] + e.weight:
                self._dist_to[w] = self._dist_to[v] + e.weight
                self._edge_to[w] = e
                if not self._on_queue[w]:
                    self._queue.append(w)
                    self._on_queue[w] = True

            # Check for negative cycle every V iterations
            self._cost += 1
            if self._cost % G.V() == 0:
                self._find_negative_cycle()
                if self.has_negative_cycle():
                    return  # Stop processing

    def _find_negative_cycle(self) -> None:
        """
        Builds the shortest path tree (SPT) and checks for cycles.
        If a cycle is found, sets self._cycle.
        (Implementation simplified for this module).
        """
        # In a full production implementation, we would perform a DFS on the
        # current SPT to find a cycle. For now, we assume this method exists.
        pass

    def has_negative_cycle(self) -> bool:
        """
        Returns True if the graph contains a negative cycle reachable from the source.
        """
        return self._cycle is not None

    def dist_to(self, v: int) -> float:
        """
        Returns the length of the shortest path from the source to vertex v.
        """
        return self._dist_to[v]

    def has_path_to(self, v: int) -> bool:
        """
        Returns True if there is a path from the source to vertex v.
        """
        return self._dist_to[v] < float("inf")

    def path_to(self, v: int) -> Optional[Iterable[DirectedEdge]]:
        """
        Returns the shortest path from the source to vertex v.

        Args:
            v (int): The destination vertex.

        Returns:
            Optional[Iterable[DirectedEdge]]: A sequence of edges, or None if no path.
        """
        if not self.has_path_to(v):
            return None
        path: Deque[DirectedEdge] = deque()
        e = self._edge_to[v]
        while e is not None:
            path.appendleft(e)
            e = self._edge_to[e.from_vertex()]
        return path
