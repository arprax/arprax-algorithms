"""
Graph Data Structures.

This module provides the core container classes for graph algorithms:
1. Graph: Undirected graph using adjacency lists.
2. Digraph: Directed graph using adjacency lists.
3. EdgeWeightedGraph: Undirected graph where edges have weights.
4. Edge: Helper class representing a weighted connection.

Implementation Details:
    - Representation: Adjacency Lists (Space complexity O(V + E)).
    - Performance:
        - Add Edge: O(1)
        - Iterate Adj: O(degree(v))
        - Check Edge: O(degree(v))
    - Self-loops and parallel edges are allowed by default.

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Section 4.1, 4.2, 4.3.
"""

from typing import List, Iterable


class Graph:
    """
    Undirected graph data structure.

    Implemented using an array of lists. Each index 'v' contains a list
    of vertices adjacent to 'v'.
    """

    def __init__(self, V: int):
        """
        Initializes an empty graph with V vertices and 0 edges.

        Args:
            V (int): Number of vertices.

        Raises:
            ValueError: If V is negative.
        """
        if V < 0:
            raise ValueError("Number of vertices must be non-negative")
        self._V = V
        self._E = 0
        # Adjacency list: _adj[v] = list of neighbors
        self._adj: List[List[int]] = [[] for _ in range(V)]

    def V(self) -> int:
        """Returns the number of vertices."""
        return self._V

    def E(self) -> int:
        """Returns the number of edges."""
        return self._E

    def add_edge(self, v: int, w: int) -> None:
        """
        Adds an undirected edge between vertices v and w.

        Args:
            v (int): First vertex.
            w (int): Second vertex.

        Raises:
            IndexError: If v or w are out of bounds.
        """
        self._validate_vertex(v)
        self._validate_vertex(w)
        self._adj[v].append(w)
        self._adj[w].append(v)
        self._E += 1

    def adj(self, v: int) -> Iterable[int]:
        """
        Returns an iterator over the vertices adjacent to vertex v.

        Args:
            v (int): The vertex.

        Returns:
            Iterable[int]: Neighbors of v.
        """
        self._validate_vertex(v)
        return self._adj[v]

    def degree(self, v: int) -> int:
        """Returns the degree of vertex v."""
        self._validate_vertex(v)
        return len(self._adj[v])

    def _validate_vertex(self, v: int) -> None:
        if v < 0 or v >= self._V:
            raise IndexError(f"Vertex {v} is not between 0 and {self._V - 1}")

    def __repr__(self) -> str:
        s = [f"{self._V} vertices, {self._E} edges\n"]
        for v in range(self._V):
            s.append(f"{v}: ")
            for w in self._adj[v]:
                s.append(f"{w} ")
            s.append("\n")
        return "".join(s)


class Digraph:
    """
    Directed graph data structure (Digraph).

    Edges are directed: add_edge(v, w) means v -> w ONLY.
    """

    def __init__(self, V: int):
        """
        Initializes an empty digraph with V vertices.

        Args:
            V (int): Number of vertices.
        """
        if V < 0:
            raise ValueError("Number of vertices must be non-negative")
        self._V = V
        self._E = 0
        self._adj: List[List[int]] = [[] for _ in range(V)]
        self._indegree: List[int] = [0] * V

    def V(self) -> int:
        """Returns the number of vertices."""
        return self._V

    def E(self) -> int:
        """Returns the number of edges."""
        return self._E

    def add_edge(self, v: int, w: int) -> None:
        """
        Adds a directed edge from v to w.

        Args:
            v (int): Source vertex.
            w (int): Destination vertex.
        """
        self._validate_vertex(v)
        self._validate_vertex(w)
        self._adj[v].append(w)
        self._indegree[w] += 1
        self._E += 1

    def adj(self, v: int) -> Iterable[int]:
        """Returns vertices pointing FROM v."""
        self._validate_vertex(v)
        return self._adj[v]

    def out_degree(self, v: int) -> int:
        """Returns the number of directed edges leaving v."""
        self._validate_vertex(v)
        return len(self._adj[v])

    def in_degree(self, v: int) -> int:
        """Returns the number of directed edges entering v."""
        self._validate_vertex(v)
        return self._indegree[v]

    def reverse(self) -> "Digraph":
        """
        Returns a new Digraph with all edges reversed.
        Useful for finding Strongly Connected Components (Kosaraju-Sharir).
        """
        R = Digraph(self._V)
        for v in range(self._V):
            for w in self.adj(v):
                R.add_edge(w, v)
        return R

    def _validate_vertex(self, v: int) -> None:
        if v < 0 or v >= self._V:
            raise IndexError(f"Vertex {v} is not between 0 and {self._V - 1}")


class Edge:
    """
    Weighted edge abstraction.
    Represents a connection between two vertices with a weight.
    Implements comparison operators for sorting (needed for Kruskal's MST).
    """

    def __init__(self, v: int, w: int, weight: float):
        self._v = v
        self._w = w
        self._weight = weight

    @property
    def weight(self) -> float:
        return self._weight

    def either(self) -> int:
        """Returns one endpoint of this edge."""
        return self._v

    def other(self, vertex: int) -> int:
        """
        Returns the other endpoint of this edge given one vertex.

        Args:
            vertex (int): One of the endpoints.

        Raises:
            ValueError: If vertex is not one of the endpoints.
        """
        if vertex == self._v:
            return self._w
        elif vertex == self._w:
            return self._v
        else:
            raise ValueError("Illegal endpoint")

    def __lt__(self, other: "Edge") -> bool:
        return self.weight < other.weight

    def __str__(self) -> str:
        return f"{self._v}-{self._w} {self._weight:.2f}"


class EdgeWeightedGraph:
    """
    Undirected graph where edges have weights.
    Used for Minimum Spanning Trees (MST) and Shortest Path algorithms.
    """

    def __init__(self, V: int):
        """Initializes empty weighted graph."""
        if V < 0:
            raise ValueError("Number of vertices must be non-negative")
        self._V = V
        self._E = 0
        self._adj: List[List[Edge]] = [[] for _ in range(V)]

    def V(self) -> int:
        return self._V

    def E(self) -> int:
        return self._E

    def add_edge(self, e: Edge) -> None:
        """
        Adds a weighted edge to the graph.

        Args:
            e (Edge): The edge object to add.
        """
        v = e.either()
        w = e.other(v)
        self._validate_vertex(v)
        self._validate_vertex(w)
        self._adj[v].append(e)
        self._adj[w].append(e)
        self._E += 1

    def adj(self, v: int) -> Iterable[Edge]:
        """Returns all weighted edges incident to vertex v."""
        self._validate_vertex(v)
        return self._adj[v]

    def edges(self) -> Iterable[Edge]:
        """Returns all edges in the graph."""
        list_edges = []
        for v in range(self._V):
            for e in self._adj[v]:
                # Only add if v is the "smaller" endpoint to avoid duplicates
                if e.other(v) > v:
                    list_edges.append(e)
        return list_edges

    def _validate_vertex(self, v: int) -> None:
        if v < 0 or v >= self._V:
            raise IndexError(f"Vertex {v} is not between 0 and {self._V - 1}")
