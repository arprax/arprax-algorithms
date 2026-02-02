# Chapter 5: Quadratic Sorts (The Testing Ground)

> **"Do not optimize prematurely. But do not be ignorant."**

## 🏛️ The Academic View
Bubble Sort, Insertion Sort, and Selection Sort are $O(N^2)$. They are "bad" algorithms used only for teaching.

## 🏗️ The Engineering Reality
Insertion Sort is the fastest algorithm in the world for $N < 32$. That is why Timsort (Python's built-in sort) switches to Insertion Sort for small chunks.

**Key Topics:**
* Implementing the "Big Three" for educational clarity.
* Benchmarking: Finding the exact $N$ where $O(N^2)$ becomes unacceptable.
