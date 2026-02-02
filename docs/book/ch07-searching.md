# Chapter 7: Searching & Hashing

> **"Finding data is easy. Finding it fast is expensive."**

## 🏛️ The Academic View
Binary Search is $O(\log N)$. Hash Tables are $O(1)$.

## 🏗️ The Engineering Reality
Binary Search requires sorted data (maintenance cost). Hash Tables require extra memory and good hash functions to avoid collisions (DDOS vulnerability).

**Key Topics:**
* **Leftmost/Rightmost Search:** Handling duplicates in production data.
* **The Hash Map:** Building a dictionary from scratch to understand collision resolution (Chaining vs. Open Addressing).
