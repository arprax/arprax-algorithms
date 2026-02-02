# Chapter 8: Binary Search Trees (BST)

> **"A tree without balance is just a linked list."**

## 🏛️ The Academic View
BSTs provide $O(\log N)$ search, insert, and delete.

## 🏗️ The Engineering Reality
Real-world data is rarely random. It often comes sorted, which turns a naive BST into a skewed $O(N)$ nightmare.

**Key Topics:**
* **The Skew Problem:** Visualizing how sorted input breaks a BST.
* **Traversal Strategies:** Writing iterative (non-recursive) traversals to avoid stack overflow.
