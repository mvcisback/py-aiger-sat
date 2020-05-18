import aiger

import aiger_sat
from aiger_sat import SolverWrapper


def test_smoke():
    x, y, z = map(aiger.atom, ['x', 'y', 'z'])
    solver = SolverWrapper()

    expr = (x & y) | ~z
    solver.add_expr(expr)
    assert solver.inputs == {'x', 'y', 'z'}
    assert len(solver.sym_table) == 3

    assert all(v in solver.sym_table for v in 'xyz')

    assert solver.unsolved

    assert solver.is_sat()

    assert not solver.unsolved
    model = solver.get_model()
    assert model is not None
    assert len(model) == 3
    assert expr(model)

    assert not solver.is_sat(assumptions={
        'x': False,
        'z': True,
    })
    assert not solver.unsolved

    core = solver.get_unsat_core()
    assert core == {'x': False, 'z': True}


def test_empty_unsat_core():
    x = aiger.atom('x')

    solver = SolverWrapper()
    solver.add_expr(x & ~x)

    assert solver.get_model() is None
    assert solver.get_unsat_core() == {}


def test_solve():
    x, y, z = map(aiger.atom, ['x', 'y', 'z'])
    model = aiger_sat.solve(x & y & z)
    assert model == {'x': True, 'y': True, 'z': True}


def test_is_sat():
    x, y, z = map(aiger.atom, ['x', 'y', 'z'])
    assert aiger_sat.is_sat(x & y & z)


def test_is_valid():
    assert aiger_sat.is_valid(aiger.atom(True))


def test_equiv():
    x, y, z = map(aiger.atom, ['x', 'y', 'z'])
    assert aiger_sat.are_equiv(x & y, x & y & (z | ~z))
