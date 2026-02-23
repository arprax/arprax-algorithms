"""
Linear Programming and the Simplex Algorithm.

This module provides an implementation of the Simplex algorithm for solving
standard-form linear programming maximization problems.

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Section 6.5.
"""

from typing import List


class Simplex:
    """
    Simplex algorithm for solving linear programming maximization problems.

    The problem is defined as:
    Maximize (c^T * x) subject to Ax <= b and x >= 0.

    This implementation uses a tableau representation and Bland's Rule to
    avoid cycling in the presence of degeneracy.
    """

    def __init__(self, a: List[List[float]], b: List[float], c: List[float]):
        """
        Initializes the Simplex solver and executes the optimization.

        Args:
            a (List[List[float]]): Constraint matrix (m x n).
            b (List[float]): Right-hand side vector (m).
            c (List[float]): Objective function coefficients (n).

        Raises:
            ValueError: If b[i] < 0 (requires a Two-Phase Simplex, not covered here).
        """
        self._m = len(b)
        self._n = len(c)

        # Check for initial feasibility (Standard form requires b >= 0)
        for val in b:
            if val < 0:
                raise ValueError("Initial solution must be feasible (b[i] >= 0)")

        # Create (m+1) x (n+m+1) tableau
        self._tableau = [[0.0] * (self._n + self._m + 1) for _ in range(self._m + 1)]

        # Populate constraints
        for i in range(self._m):
            for j in range(self._n):
                self._tableau[i][j] = float(a[i][j])
            # Add slack variables
            self._tableau[i][self._n + i] = 1.0
            self._tableau[i][self._n + self._m] = float(b[i])

        # Populate objective function (bottom row)
        for j in range(self._n):
            self._tableau[self._m][j] = float(c[j])

        self._solve()

    def _solve(self) -> None:
        """Main loop of the Simplex algorithm."""
        while True:
            # Find entering column (using Bland's Rule: smallest index with positive coeff)
            q = self._bland_entering_col()
            if q == -1:
                break  # Optimal solution reached

            # Find leaving row (Minimum Ratio Test)
            p = self._min_ratio_test(q)
            if p == -1:
                raise ArithmeticError("Linear program is unbounded")

            # Pivot on entry (p, q)
            self._pivot(p, q)

    def _bland_entering_col(self) -> int:
        """Finds entering column using Bland's rule to prevent cycling."""
        for j in range(self._n + self._m):
            if (
                self._tableau[self._m][j] > 1e-10
            ):  # Using epsilon for floating point stability
                return j
        return -1

    def _min_ratio_test(self, q: int) -> int:
        """Finds leaving row using the minimum ratio test."""
        p = -1
        for i in range(self._m):
            if self._tableau[i][q] <= 1e-10:
                continue
            if p == -1:
                p = i
            elif (
                self._tableau[i][self._n + self._m] / self._tableau[i][q]
                < self._tableau[p][self._n + self._m] / self._tableau[p][q]
            ):
                p = i
        return p

    def _pivot(self, p: int, q: int) -> None:
        """Performs a pivot operation on the tableau entry (p, q)."""
        # Scale pivot row
        pivot_val = self._tableau[p][q]
        for j in range(self._n + self._m + 1):
            self._tableau[p][j] /= pivot_val

        # Eliminate other rows
        for i in range(self._m + 1):
            if i != p:
                factor = self._tableau[i][q]
                for j in range(self._n + self._m + 1):
                    self._tableau[i][j] -= factor * self._tableau[p][j]

    def value(self) -> float:
        """Returns the maximum value of the objective function."""
        return -self._tableau[self._m][self._n + self._m]

    def primal(self) -> List[float]:
        """Returns the optimal primal solution vector x."""
        x = [0.0] * self._n
        for j in range(self._n):
            # Check if column is a basis column
            row = -1
            is_basis = True
            for i in range(self._m + 1):
                if abs(self._tableau[i][j]) > 1e-10:
                    if self._tableau[i][j] == 1.0 and row == -1:
                        row = i
                    else:
                        is_basis = False
                        break
            if is_basis and row != -1 and row < self._m:
                x[j] = self._tableau[row][self._n + self._m]
        return x
