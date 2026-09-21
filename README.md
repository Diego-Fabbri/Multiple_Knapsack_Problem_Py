# Multiple Knapsack Problem (MKP)

A **Mixed Integer Linear Programming (MILP)** model in **Python** for the **Multiple Knapsack Problem**, built with the **[Pyomo](http://www.pyomo.org/)** optimization framework and solved via the **IBM ILOG CPLEX** solver.

## Overview

The Multiple Knapsack Problem (MKP) is a classic combinatorial optimization problem in Operations Research. Given a set of items, each with a known weight and value, and a set of knapsacks, each with a fixed capacity, the goal is to **select which items to assign to which knapsack** so as to **maximize the total value** of selected items — without exceeding any knapsack's capacity.

Unlike the Bin Packing Problem, the MKP has a fixed number of knapsacks and items may be **left unassigned** when they cannot all fit. Unlike the standard single-knapsack problem, items must be distributed across **multiple knapsacks** with independent capacities. The MKP is NP-hard and has applications in resource allocation, cargo loading, budget planning, and project selection.

## Repository Contents

| File | Description |
|---|---|
| `Multiple_Knapsack_Problem.py` | Python script implementing and solving the MKP via Pyomo and CPLEX |
| `Multiple_Knapsack_Problem_Results.txt` | Solver output: execution time, status, optimal value, and item assignments per knapsack |
| `Multiple_Knapsack_Problem.pdf` | Mathematical formulation of the problem |

## Mathematical Formulation

### Parameters

- $n$ = number of items (index $i = 1, \dots, n$)
- $m$ = number of knapsacks (index $j = 1, \dots, m$)
- $w_i$ = weight of item $i$; $\forall\, i = 1, \dots, n$
- $v_i$ = value of item $i$; $\forall\, i = 1, \dots, n$
- $C_j$ = capacity of knapsack $j$; $\forall\, j = 1, \dots, m$

### Variable

- $x_{ij}$ = binary assignment variable:

$$
x_{ij} = \begin{cases} 1 & \text{if item } i \text{ is placed in knapsack } j \\ 0 & \text{otherwise} \end{cases}
$$

### Objective Function

**(1)** — Maximize total value of selected items

$$
\displaystyle \max \sum_{i=1}^{n} \sum_{j=1}^{m} v_i \cdot x_{ij}
$$

### Constraints

**(2)** — Capacity: the total weight of items assigned to each knapsack cannot exceed its capacity

$$
\displaystyle \sum_{i=1}^{n} w_i \cdot x_{ij} \le C_j \qquad \forall\, j = 1, \dots, m
$$

**(3)** — Each item can be assigned to at most one knapsack

$$
\displaystyle \sum_{j=1}^{m} x_{ij} \le 1 \qquad \forall\, i = 1, \dots, n
$$

**(4)** — Binary assignment variables

$$
x_{ij} \in \{0, 1\} \qquad \forall\, i = 1, \dots, n,\ j = 1, \dots, m
$$

> **Note on constraint (3):** The inequality $\le 1$ (rather than $= 1$) allows items to be left unassigned when there is insufficient capacity to include them profitably. The model selects the most valuable subset of items that can be feasibly distributed across the available knapsacks.

A copy of this formulation is also available as a standalone PDF in this repository.

## Example Instance

The script uses a hardcoded instance with **15 items** and **5 knapsacks**, each with capacity $C_j = 100$:

| Item | Weight $w_i$ | Value $v_i$ |
|:---:|---:|---:|
| 0 | 48 | 10 |
| 1 | 30 | 30 |
| 2 | 42 | 25 |
| 3 | 36 | 50 |
| 4 | 36 | 35 |
| 5 | 48 | 30 |
| 6 | 42 | 15 |
| 7 | 42 | 40 |
| 8 | 36 | 30 |
| 9 | 24 | 35 |
| 10 | 30 | 45 |
| 11 | 30 | 10 |
| 12 | 42 | 20 |
| 13 | 36 | 30 |
| 14 | 36 | 25 |
| **Total** | **558** | **430** |

- **Knapsack capacity**: $C_j = 100$ for all $j = 0, \dots, 4$
- **Total capacity**: $5 \times 100 = 500$ units
- **Total item weight**: $558$ units — exceeds total capacity by $58$ units, so 3 items must be left out

The **optimal total value is 395**, found in **0.17 seconds**. Items 0, 6, and 11 are excluded (lowest value-to-weight ratios). The optimal assignments are:

| Knapsack | Items | Packed weight | Packed value |
|:---:|:---:|---:|---:|
| 0 | 4, 8, 9 | 96 | 100 |
| 1 | 7, 13 | 78 | 70 |
| 2 | 1, 10, 14 | 96 | 100 |
| 3 | 3, 5 | 84 | 80 |
| 4 | 2, 12 | 84 | 45 |
| **Total** | **12 items** | **438** | **395** |

Average knapsack utilization: **87.6%** (438 / 500). The set of selected items is the same as the Java version, but the distribution across knapsacks differs — both are valid optimal solutions since the MKP may admit multiple packings with the same maximum value.

## Requirements

Install the required Python packages via pip:

```bash
pip install pyomo numpy pandas
```

**IBM ILOG CPLEX** must also be installed separately on your system. An academic license is available free of charge through the [IBM Academic Initiative](https://www.ibm.com/academic).

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Diego-Fabbri/Multiple_Knapsack_Problem_Py.git
   cd Multiple_Knapsack_Problem_Py
   ```

2. Run the script:
   ```bash
   python Multiple_Knapsack_Problem.py
   ```

## Output

When executed, the script:
- Builds the MILP model using Pyomo's `ConcreteModel` and prints the full model structure to the console
- Solves it via CPLEX and measures execution time
- Writes the results to `Multiple_Knapsack_Problem_Results.txt`, including:
  - Execution time in seconds
  - Solver status and termination condition
  - Optimal total packed value (objective)
  - For each knapsack: list of assigned items with individual weights and values, plus total packed weight and value
  - Total packed weight across all knapsacks
