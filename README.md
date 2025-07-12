# Wordle Solver & Benchmark  
*A fast, statistics-driven Wordle bot that averages **3.60 guesses** per puzzle (better than the reported human average of 3.97).*

---

## Overview
This repository contains:

| File | Purpose |
|------|---------|
| `eval.py` | Core solver. Plays Wordle for a single target word and prints the guess count. |
| `bench.py` | Benchmarks solver across a curated word list and reports the rolling / final average. |
| `wordle.py` | Lightweight emulation of the official Wordle rules (green / yellow / gray logic, victory detection, ANSI coloring). |

---

## Quick Start

```bash
# 1. Clone & enter
git clone https://github.com/your-handle/wordle-solver.git
cd wordle-solver

# 2. (Optional) create a venv
python3 -m venv venv
source venv/bin/activate

# 3. Install runtime deps (only stdlib required)
pip install --upgrade pip

# 4. Solve a single puzzle
python3 eval.py crane          # uses default probing word "aeros"
python3 eval.py crane raise    # custom probing word "raise"

# 5. Run full benchmark
python3 bench.py