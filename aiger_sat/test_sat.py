import aiger

from aiger_sat import SolverWrapper


def test_sat():
    x, y, z = map(aiger.atom, ['x', 'y', 'z'])
    solver = SolverWrapper()

    expr = (x & y) | ~z
    solver.add_expr(expr)
    assert solver.inputs == {'x', 'y', 'z'}
    assert solver.max_var > 3
    assert len(solver.sym_table) == 3

    assert all(v in solver.sym_table for v in 'xyz')

    assert solver.unsolved

    assert solver.is_sat()

    assert not solver.unsolved
    model = solver.get_model()
    assert model is not None
    assert len(model) == 3
    assert expr(model)


def test_unsat():
    x, y, z = map(aiger.atom, ['x', 'y', 'z'])
    solver = SolverWrapper()

    expr = (x & y & z) | x
    solver.add_expr(expr)
    assert solver.inputs == {'x', 'y', 'z'}
    assert solver.max_var > 3
    assert len(solver.sym_table) == 3

    assert all(v in solver.sym_table for v in 'xyz')

    assert solver.unsolved

    assert not solver.is_sat(assumptions={'x': False})
    assert not solver.unsolved

    model = solver.get_model()
    assert model is None

    core = solver.get_unsat_core()
    assert core is not None
    assert core == {'x': False}
