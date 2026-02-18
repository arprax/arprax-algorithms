# Arprax Algorithms

**Industrial-grade algorithms, performance profilers, and data structures for Python.**

Built by **Arprax Lab**, this toolkit is designed for the "Applied Data Intelligence" era—where understanding how code scales is as important as the code itself.

---

## 🚀 Features

* **ArpraxProfiler:** High-precision analysis with GC control, warmup cycles, and OHPV2 (Doubling Test) complexity estimation.
* **Industrial Utils:** High-performance data factories (random_array, sorted_array) for robust benchmarking.
* **Standard Library:** High-performance implementations of classic algorithms (Merge Sort, Bubble Sort, etc.) with strict type hinting.

## 📦 Installation

```bash
# Core only
pip install arprax-algorithms

# With visual tools
pip install arprax-algorithms[visuals]

# With research tools
pip install arprax-algorithms[research]
```

## 🔬 Quick Start: Benchmarking

Once installed, you can immediately run a performance battle between algorithms.

```python
from arprax.algos import Profiler
from arprax.algos.utils import random_array  # Clean import from your new 'utils'
from arprax.algos.algorithms import merge_sort # Using the 'lifted' API

# 1. Initialize the industrial profiler
profiler = Profiler(mode="min", repeats=5)

# 2. Run a doubling test (OHPV2 Analysis)
results = profiler.run_doubling_test(
    merge_sort,
    random_array,
    start_n=500,
    rounds=5
)

# 3. Print the performance analysis
profiler.print_analysis("Merge Sort", results)
```
We've included a performance profiler demo in the root directory. To see the library in action:
```bash
python demo_profiler.py
```

We've included a visualization demo in the root directory. To see the library in action:
```bash
python demo_visualizer.py
```

## 🏗️ The Arprax Philosophy

> **Applied Data Intelligence requires more than just code—it requires proof.**

* **Zero-Magic:** Every algorithm is written for clarity and performance. We don't hide logic behind obscure abstractions or hidden standard library calls.
* **Empirical Evidence:** We don't just guess Big O complexity; we measure it using high-resolution timers and controlled environments.
* **Industrial Scale:** Our tools are designed to filter out background CPU noise, providing reliable benchmarks for real-world software engineering.

## 📚 Citation

**To cite the Software:**
See the "Cite this repository" button on our [GitHub](https://github.com/arprax/arprax-algorithms).

**To cite the Handbook (Documentation):**

```bibtex
@manual{arprax_handbook,
  title        = {The Algorithm Engineering Handbook},
  author       = {Chowdhury, Tanmoy},
  organization = {Arprax LLC},
  year         = {2026},
  url          = {https://algorithms.arprax.com/book},
  note         = {Accessed: 2026-02-01}
}
```

---

**© 2026 Arprax Lab** *A core division of Arprax dedicated to Applied Data Intelligence.*