# py-aiger-sat
Pythonic interface between AIGs and SAT solvers.

[![Build Status](https://cloud.drone.io/api/badges/mvcisback/py-aiger-sat/status.svg)](https://cloud.drone.io/mvcisback/py-aiger-sat)
[![codecov](https://codecov.io/gh/mvcisback/py-aiger-sat/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/py-aiger-sat)
[![PyPI version](https://badge.fury.io/py/py-aiger-sat.svg)](https://badge.fury.io/py/py-aiger-sat)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)

<!-- markdown-toc end -->


# Installation

If you just need to use `aiger_sat`, you can just run:

`$ pip install py-aiger-sat`

For developers, note that this project uses the
[poetry](https://poetry.eustace.io/) python package/dependency
management tool. Please familarize yourself with it and then
run:

`$ poetry install`

# Usage

`aiger_sat` has two seperate API's. The first, called the Object API,
centers around the `SolverWrapper` object - a thin wrapper around a
`pysat` solver. The second is a Function API which exposes 4 functions
`solve`, `is_sat`, `is_valid`, and `are_equiv`. The function API is
primarily useful for simple 1-off SAT instances, where as the object
API is more useful when incremental solves are needed, or the
underlying `pysat` solver must be exposed.

## Object API

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

## Function API

```python
import aiger
import aiger_sat

x, y, z = map(aiger.atom, ['x', 'y', 'z'])
assert aiger_sat.is_sat(x & y & z)

model = aiger_sat.solve(x & y & z)
assert model == {'x': True, 'y': True, 'z': True}

assert aiger_sat.is_valid(aiger.atom(True))

expr1 = x & y
expr2 = x & y & (z | ~z)
assert aiger_sat.are_equiv(expr1, expr2)
```
