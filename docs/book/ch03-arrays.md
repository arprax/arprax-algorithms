# Chapter 3: Dynamic Arrays & Linked Lists

> **"Memory is not a continuous tape. It is a fragmented landscape."**

## 🏛️ The Academic View
Arrays give $O(1)$ access. Linked Lists give $O(1)$ insertion. We treat memory as an abstract resource.

## 🏗️ The Engineering Reality
Python Lists are dynamic arrays of pointers. They are cache-friendly but memory-heavy. Linked Lists in Python are often disastrous for performance due to pointer chasing and cache misses.

**Key Topics:**
* The hidden cost of `list.append()` (Amortized analysis).
* Why `sys.getsizeof()` lies to you.
* Implementing a custom Linked List only when strictly necessary.
