from functools import wraps
from typing import Callable, Hashable, TypeVar, Set

import aiger
import attr
import funcy as fn
from aiger_cnf import aig2cnf
from pysat.solvers import Glucose4
from bidict import bidict


Solver = TypeVar("Solver")


def _require_solved(func):
    @wraps(func)
    def decorated(self, *args, **kwargs):
        if self.unsolved:
            self.solver.solve()

        return func(self, *args, **kwargs)
    return decorated


def id_pool_factory():
    max_var = 0

    @fn.memoize
    def _fresh(val):
        nonlocal max_var
        max_var += 1
        return max_var

    return _fresh


@attr.s(auto_attribs=True)
class SolverWrapper:
    solver: Solver = attr.ib(factory=Glucose4)
    unsolved: bool = True
    inputs: Set[str] = attr.ib(factory=set)
    sym_table: bidict = attr.ib(factory=bidict)
    _id_pool: Callable[[Hashable], int] = attr.ib(factory=id_pool_factory)

    def add_expr(self, expr):
        expr = aiger.BoolExpr(expr.aig)
        self.unsolved = True
        self.inputs |= expr.inputs
        cnf = aig2cnf(expr, fresh=self._id_pool)
        for clause in cnf.clauses:
            self.solver.add_clause(clause)
        self.sym_table.update(cnf.input2lit)

    def is_sat(self, assumptions=None):
        if assumptions is None:
            assumptions = {}

        assumptions = [
            (1 if v else -1)*self.sym_table[k] for k, v in assumptions.items()
        ]

        self.unsolved = False
        return self.solver.solve(assumptions)

    def _translate(self, cube):
        if cube is None:
            return cube

        idx2sym = self.sym_table.inv
        return {
            idx2sym[abs(v)]: v > 0 for v in cube
            if abs(v) in idx2sym and idx2sym[abs(v)] in self.inputs
        }

    @_require_solved
    def get_model(self):
        model = self.solver.get_model()
        return self._translate(model)

    @_require_solved
    def get_unsat_core(self):
        core = self._translate(self.solver.get_core())
        return {} if (core is None) else core


def _solve(expr, method, engine, wrapper=SolverWrapper):
    solver = wrapper(engine())
    solver.add_expr(expr)
    return method(solver)


def solve(expr, *, engine=Glucose4, wrapper=SolverWrapper):
    return _solve(expr, wrapper.get_model, engine=engine, wrapper=wrapper)


def is_sat(expr, *, engine=Glucose4):
    return _solve(expr, SolverWrapper.is_sat, engine=engine)


def is_valid(expr, *, engine=Glucose4):
    return not is_sat(~expr, engine=engine)


def are_equiv(expr1, expr2, *, engine=Glucose4):
    # Make sure they're expressions.
    assert len(expr1.aig.outputs) == len(expr2.aig.outputs) == 1
    expr1, expr2 = map(lambda e: aiger.BoolExpr(e.aig), (expr1, expr2))

    return is_valid(expr1 == expr2)
