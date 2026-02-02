# Chapter 9: Graph Theory

> **"The world is not a list. It is a network."**

## 🏛️ The Academic View
Graphs are sets of Vertices ($V$) and Edges ($E$). We represent them with Adjacency Matrices.

## 🏗️ The Engineering Reality
Adjacency Matrices explode memory usage ($V^2$). In Python, we model sparse graphs using `Dict[Node, List[Node]]`.

**Key Topics:**
* **Social Graphs:** Modeling relationships.
* **BFS vs. DFS:** When to crawl wide (Web Scrapers) vs. when to crawl deep (Maze Solvers).
