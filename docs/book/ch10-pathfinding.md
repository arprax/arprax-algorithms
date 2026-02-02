# Chapter 10: Pathfinding

> **"The shortest path is not always the fastest."**

## 🏛️ The Academic View
Dijkstra's Algorithm finds the shortest path in a weighted graph.

## 🏗️ The Engineering Reality
Dijkstra searches in a circle. In the real world (Maps), we know the destination's direction. We need **A*** (A-Star) to prioritize the search.

**Key Topics:**
* **Heuristics:** Teaching the algorithm to "guess" effectively.
* **Priority Queues:** Optimizing the "Open Set" using `heapq`.
