# Chapter 2: The Profiling Mindset

> **"Big-O tells you how it scales. Profiling tells you how it runs."**

## 🏛️ The Academic View
We teach that $O(1)$ is always better than $O(N)$. We ignore constants ($C$) and hardware constraints.

## 🏗️ The Engineering Reality
A complex $O(1)$ hash lookup can be slower than a simple $O(N)$ loop for small $N$ due to CPU caching and hash collision overhead.

In this chapter, we build the **ArpraxProfiler**:
* Measuring **Wall-Clock Time** vs. **CPU Time**.
* Tracing memory allocation (Heap pressure).
* Visualizing the "Crossover Point" where asymptotic complexity matters.
