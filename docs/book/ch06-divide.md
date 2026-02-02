# Chapter 6: Divide & Conquer

> **"Divide the problem. Conquer the complexity."**

## 🏛️ The Academic View
Merge Sort guarantees $O(N \log N)$. Quick Sort is $O(N^2)$ in the worst case but "usually faster."

## 🏗️ The Engineering Reality
The difference between **Stable** and **Unstable** sorting destroys data integrity in production pipelines.

**Key Topics:**
* **Stability:** Why Merge Sort preserves the order of equal elements (crucial for multi-column sorting).
* **Recursion Depth:** Handling `RecursionError` in Python when dividing too deep.
