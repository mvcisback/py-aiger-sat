# py-aiger-sat
Pythonic interface between AIGs and SAT solvers.

## Usage

The primary entry point for `aiger_sat` is the `SolverWrapper` object
which is a thin wrapper around a `pysat` solver.


```python
from aiger_sat import SolverWrapper

solver = SolverWrapper()  # defaults to Glucose4

from pysat.solver import Glucose3
solver2 = SolverWrapper(solver=Glucose3)
```

`solver` operate on boolean expressions in the form of `aiger`
circuits with a single output. For example,


```python
import aiger

x, y, z = map(aiger.atom, ['x', 'y', 'z'])

expr = (x & y) | ~z
solver.add_expr(expr)
assert solver.is_sat()
model = solver.get_model()
print(model)  # {'x': True, 'y': False, 'z': False}
assert expr(model)
```

Further, `aiger_sat` supports making assumptions and computing
unsat_cores.

```python
# Make invalid assumption.
assert not solver.is_sat(assumptions={
    'x': False,
    'z': True,
})
assert not solver.unsolved

core = solver.get_unsat_core()
assert core == {'x': False, 'z': True}
```
