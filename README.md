# PyLKH
This is a super simple Python wrapper for the constrained traveling salesman and vehicle routing problem solver called [LKH-3](http://akira.ruc.dk/~keld/research/LKH-3/).

If you want to use this wrapper, you should [install](http://akira.ruc.dk/~keld/research/LKH-3/) LKH-3 first.

LKH-3 expects problems in the [TSPLIB95](https://github.com/ben-hudson/pylkh/blob/master/tsplib95.pdf) format. Using PyLKH you can solve problems represented as Python objects (via [tsplib95](https://tsplib95.readthedocs.io/)) or files.

> CAUTION: distances are represented by integer values in the TSPLIB format. This can produce unexpected behaviour for some problems, like those with all nodes within the unit square. The `precision` parameter controls this. More information [here](https://github.com/ben-hudson/pylkh/blob/master/LKH_guide.pdf) (pg. 6).

## Install
```
pip install lkh
```

## Example
```
import requests
import tsplib95
import lkh

problem_str = requests.get('http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n32-k5.vrp').text
problem = tsplib95.parse(problem_str)

solver_path = '../LKH-3.0.6/LKH'
lkh.solve(solver_path, problem=problem, max_trials=10000, runs=10)
```
Output:
```
[[26, 7, 13, 17, 19, 31, 21],
 [24, 27],
 [14, 28, 11, 4, 23, 3, 2, 6],
 [29, 18, 8, 9, 22, 15, 10, 25, 5, 20],
 [12, 1, 16, 30]]
```

## API
```lkh.solve(solver='LKH', problem=None, **kwargs)```

Solve a problem.

### Parameters
**solver** (str, optional): Path to LKH-3 executable.

**problem** ([tsplib95.model.StandardProblem](https://tsplib95.readthedocs.io/en/stable/pages/modules.html#tsplib95.models.StandardProblem), optional): Problem object. `problem` or `problem_file` is required.

**quiet** (bool, optional): Suppress LKH-3 output.

**kwargs** (optional): Any LKH-3 parameter described [here](https://github.com/ben-hudson/pylkh/blob/master/LKH_guide.pdf) (pg. 5-7). Lowercase works. For example: `runs=10`.

### Returns
**routes** (list): List of lists of nodes.
