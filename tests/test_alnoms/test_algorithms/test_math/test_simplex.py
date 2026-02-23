import pytest
from alnoms.algorithms.math.simplex import Simplex


def test_simplex_standard_max():
    """Test a standard maximization problem."""
    # Maximize 13x + 23y
    # s.t. 5x + 15y <= 480
    #      4x + 4y  <= 160
    #      35x + 20y <= 1190
    a = [[5, 15], [4, 4], [35, 20]]
    b = [480, 160, 1190]
    c = [13, 23]

    lp = Simplex(a, b, c)
    assert pytest.approx(lp.value(), rel=1e-5) == 800.0
    x = lp.primal()
    # Solution x=12, y=28
    assert pytest.approx(x[0], rel=1e-5) == 12.0
    assert pytest.approx(x[1], rel=1e-5) == 28.0


def test_simplex_unbounded():
    """Test an unbounded linear program."""
    a = [[-1, 1]]
    b = [1]
    c = [1, 1]  # Increasing either increases obj infinitely

    with pytest.raises(ArithmeticError, match="unbounded"):
        Simplex(a, b, c)


def test_simplex_invalid_b():
    """Test feasibility check (negative b)."""
    with pytest.raises(ValueError, match="feasible"):
        Simplex([[1]], [-1], [1])


def test_simplex_non_basis_coverage():
    """
    Forces coverage of non-basis variable logic in primal().
    In this problem, x2 will be 0 (non-basic).
    """
    # Maximize 3x1 + 5x2
    # s.t. 1x1 + 0x2 <= 4
    #      0x1 + 2x2 <= 12
    #      3x1 + 2x2 <= 18
    a = [[1, 0], [0, 2], [3, 2]]
    b = [4, 12, 18]
    c = [3, 5]

    lp = Simplex(a, b, c)
    x = lp.primal()

    # x1=2, x2=6 -> Value = 3(2) + 5(6) = 36
    assert pytest.approx(lp.value()) == 36.0
    assert x[0] == 2.0
    assert x[1] == 6.0


def test_simplex_degenerate_and_small_values():
    """
    Covers epsilon checks and variables that don't enter the basis.
    """
    # Maximize x + y
    # s.t. x <= 1
    # y is not in any constraint, but has a small objective coeff
    a = [[1, 0]]
    b = [1]
    c = [1, 1e-11]  # Very small coefficient should be ignored by epsilon

    lp = Simplex(a, b, c)
    assert pytest.approx(lp.value()) == 1.0
    assert lp.primal()[1] == 0.0  # Should remain 0


def test_simplex_non_basis_column_logic():
    """
    Specifically targets lines 128-129 in simplex.py.
    Forces the primal() method to encounter a non-basis column
    with multiple non-zero entries to trigger the 'break' logic.
    """
    # Maximize 2x + y
    # s.t. x <= 4
    #      x + y <= 8
    # In the optimal tableau, one of the slack variables
    # will likely become non-basic and have multiple non-zero
    # entries in its column.
    a = [[1, 0], [1, 1]]
    b = [4, 8]
    c = [2, 1]

    lp = Simplex(a, b, c)
    x = lp.primal()

    # Expected: x=4, y=4, Value=12
    assert pytest.approx(lp.value()) == 12.0
    assert x[0] == 4.0
    assert x[1] == 4.0


def test_simplex_zero_coefficient_coverage():
    """
    Ensures that variables with a 0 coefficient in the objective
    function but that are part of constraints are handled.
    """
    a = [[1, 1]]
    b = [5]
    c = [1, 0]  # y has 0 coefficient

    lp = Simplex(a, b, c)
    x = lp.primal()
    assert x[0] == 5.0
    assert x[1] == 0.0
