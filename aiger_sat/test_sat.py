import aiger

from aiger_sat import SolverWrapper


def test_smoke():
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

    assert not solver.is_sat(assumptions={
        'x': False,
        'z': True,
    })
    assert not solver.unsolved

    core = solver.get_unsat_core()
    assert core == {'x': False, 'z': True}
