from aiger_bv import atom

from aiger_sat import sat_bv


def test_get_model():
    expr = atom(4, 'x') & atom(4, 'y') < 2
    f = sat_bv.SolverBVWrapper()
    f.add_expr(expr)

    model = f.get_model()
    assert len(model) == 2
    assert expr(model)


def test_solve():
    expr = atom(4, 'x') & atom(4, 'y') < 2
    model = sat_bv.solve(expr)
    assert len(model) == 2
    assert expr(model)
