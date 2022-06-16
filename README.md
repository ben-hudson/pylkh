# PyLKH
This is a super simple Python wrapper for the constrained traveling salesman and vehicle routing problem solver called [LKH-3](http://akira.ruc.dk/~keld/research/LKH-3/).

If you want to use this wrapper, you need to install LKH-3 first. For example, on Ubuntu:
```
wget http://akira.ruc.dk/~keld/research/LKH-3/LKH-3.0.6.tgz
tar xvfz LKH-3.0.6.tgz
cd LKH-3.0.6
make
sudo cp LKH /usr/local/bin
```

LKH-3 expects problems in the [TSPLIB](https://github.com/ben-hudson/pylkh/blob/master/docs/tsplib.pdf) format.
It extends the format [to support VRPs](https://github.com/ben-hudson/pylkh/blob/master/docs/lkh-3.pdf).

Using PyLKH you can solve problems represented as Python objects or files.

> CAUTION: distances are represented by integer values in the TSPLIB format. This can produce unexpected behaviour for some problems, like those with all nodes within the unit square. You can scale all coordinates by a large number to avoid this.

## Install
```
pip install lkh
```

## Example
```
import requests
import lkh

problem_str = requests.get('http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n32-k5.vrp').text
problem = lkh.LKHProblem.parse(problem_str)

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
### ```lkh.solve(solver='LKH', problem=None, problem_file=None, **kwargs)```

Solve a problem.

#### Parameters
**solver** (optional): Path to LKH-3 executable. Defaults to `LKH`.

**problem** (optional): Problem object. [LKHProblem](https://github.com/ben-hudson/pylkh/blob/master/lkh/problems.py#L28) is preferred but [tsplib95.models.StandardProblem](https://tsplib95.readthedocs.io/en/stable/pages/modules.html#tsplib95.models.StandardProblem) also works. `problem` or `problem_file` is required.

**problem_file** (optional): Path to TSPLIB-formatted problem. `problem` or `problem_file` is required.

**kwargs** (optional): Any LKH-3 parameter described [here](https://github.com/ben-hudson/pylkh/blob/master/docs/lkh.pdf) (pg. 5-7) or [here](https://github.com/ben-hudson/pylkh/blob/master/docs/lkh-3.pdf) (pg. 6-8). Lowercase works. For example: `runs=10`.

#### Returns
**routes** (list): List of lists of nodes.

### ```class lkh.LKHProblem```

Problem supporting fields described [here](https://github.com/ben-hudson/pylkh/blob/master/docs/lkh-3.pdf) (pg. 4-6). Inherits from [tsplib95.models.StandardProblem](https://tsplib95.readthedocs.io/en/stable/pages/modules.html#tsplib95.models.StandardProblem).

The available specification fields are:
* `NAME`
* `TYPE`
* `COMMENT`
* `DIMENSION`
* `CAPACITY`
* `EDGE_WEIGHT_TYPE`
* `EDGE_WEIGHT_FORMAT`
* `EDGE_DATA_FORMAT`
* `NODE_COORD_TYPE`
* `DISPLAY_DATA_TYPE`
* `SALESMEN`
* `VEHICLES`
* `DISTANCE`
* `RISK_THRESHOLD`
* `SCALE`

The available data fields are:
* `NODE_COORD_SECTION`
* `DEPOT_SECTION`
* `DEMAND_SECTION`
* `EDGE_DATA_SECTION`
* `FIXED_EDGES_SECTION`
* `DISPLAY_DATA_SECTION`
* `TOUR_SECTION`
* `EDGE_WEIGHT_SECTION`
* `BACKHAUL_SECTION`
* `PICKUP_AND_DELIVERY_SECTION`
* `SERVICE_TIME_SECTION`
* `TIME_WINDOW_SECTION`
