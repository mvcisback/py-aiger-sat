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
