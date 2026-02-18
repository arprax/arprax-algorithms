# 🎓 Arprax Lab: Algorithm Demonstrations

Welcome to the **Arprax Lab** demonstration suite. This directory contains high-fidelity examples designed to help students and researchers visualize, profile, and interact with the algorithms contained in the `arprax-algorithms` core library.

---

## 🚀 Overview

These examples are decoupled from the core library to ensure that the production package remains zero-dependency and lightweight. To run these demonstrations, you will need to install the optional scientific visualization stack.



---

## 🛠️ Installation

Before running the examples, ensure you have the `visuals` extras installed in your environment:

```bash
pip install "arprax-algorithms[visuals]"
```
---

> [!IMPORTANT]
> This will install **Matplotlib** and **NetworkX**, which are required for the real-time animations.

## 📚 Available Demonstrations

### 1. Algorithm Visualizer (`visualizer.py`)
This script provides real-time, frame-by-frame animations of sorting and search logic. It is the primary tool for the **Arprax Academy** curriculum to demonstrate algorithmic complexity visually.

**How to run:**
```bash
python examples/visualizer.py
```

---

> [!IMPORTANT]
> To run these demonstrations, you must have the `visuals` extras installed. This includes **Matplotlib** and **NetworkX**, which are required for real-time animations and graph rendering.

```bash
pip install "arprax-algorithms[visuals]"
```

- Key Features: Real-time bar-chart animations for sorting and dynamic graph traversal for linked lists.

### 2. Performance Profiler (`profiler_demo.py`)
A demonstration of the `ArpraxProfiler`, showing how to measure execution time, memory usage, and operation counts across different input sizes ($N$). This tool is essential for verifying theoretical Big O complexity with empirical data.



**How to run:**
```bash
python examples/profiler_demo.py
```
Key Features:
- Automatic Table Generation: Outputs clean Markdown or ASCII tables for easy documentation.
- Time-Complexity Reporting: Compares $O(1)$, $O(N)$, $O(\log N)$, and $O(N^2)$ behaviors.
- Resource Tracking: High-precision memory and CPU delta measurement.
---
## 🧪 Running Manual Tests
If you are contributing to the visualization logic, you can run the manual test suite located in the tests/manual/ directory. Note that these tests are excluded from the standard CI/CD pipeline because they require a GUI environment.
```Bash
pytest tests/manual/test_visuals.py
```
---

## ⚖️ Architecture Note

> "In **Arprax Lab**, we prioritize **Modular Decoupling**. By keeping our visualization logic in the `examples/` layer, we maintain a 100% verified core library while providing a rich, interactive educational experience."



---
*Developed by **Arprax Lab** for **Arprax Academy**.*