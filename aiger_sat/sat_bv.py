try:
    import aiger_bv
except ModuleNotFoundError:
    raise ModuleNotFoundError("Please install with bitvector option.")

import attr
from pysat.solvers import Glucose4

import aiger_sat


@attr.s(slots=True, auto_attribs=True)
class SolverBVWrapper(aiger_sat.SolverWrapper):
    bmap: aiger_bv.bundle.BundleMap = aiger_bv.bundle.BundleMap()

    def add_expr(self, expr):
        super().add_expr(expr)
        self.bmap += expr.aigbv.imap

    def get_model(self):
        model = {n: size*(False,) for n, size in self.bmap.items()}
        model = self.bmap.blast(model)
        model.update(super().get_model())
        return self.bmap.unblast(model)


def solve(expr, *, engine=Glucose4):
    return aiger_sat.solve(expr, engine=engine, wrapper=SolverBVWrapper)
