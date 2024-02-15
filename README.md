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

> __CAUTION:__ distances are represented by integer values in the TSPLIB format. This can produce unexpected behaviour for some problems, like those with all nodes within the unit square. You can use the `EXACT_2D` distance to avoid rounding issues.

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
Output (values correspond to nodes, which are 1-indexed, _not_ node indicies, which are 0-indexed):
```
[[27, 8, 14, 18, 20, 32, 22],
 [25, 28],
 [15, 29, 12, 5, 24, 4, 3, 7],
 [30, 19, 9, 10, 23, 16, 11, 26, 6, 21],
 [13, 2, 17, 31]]
```

## API
### ```lkh.solve(solver='LKH', problem=None, problem_file=None, **kwargs)```

Solve a problem instance.

#### Parameters
* __solver__ (optional): Path to LKH-3 executable. Defaults to `LKH`.

* __problem__ (optional): Problem object. [LKHProblem](https://github.com/ben-hudson/pylkh/blob/master/lkh/problems.py#L28) is preferred but [tsplib95.models.StandardProblem](https://tsplib95.readthedocs.io/en/stable/pages/modules.html#tsplib95.models.StandardProblem) also works. `problem` or `problem_file` is required.

* __problem_file__ (optional): Path to TSPLIB-formatted problem. `problem` or `problem_file` is required.

* __kwargs__ (optional): Any LKH-3 parameter described [here](https://github.com/ben-hudson/pylkh/blob/master/docs/lkh.pdf) (pg. 5-7) or [here](https://github.com/ben-hudson/pylkh/blob/master/docs/lkh-3.pdf) (pg. 6-8). Lowercase works. For example: `runs=10`.

#### Returns
__routes__: List of lists of nodes (nodes, *not* node indicies).

### _class_ ```lkh.LKHProblem```

A problem that can be solved by LKH-3. Fields are (partially) described [here](https://github.com/ben-hudson/pylkh/blob/master/docs/lkh-3.pdf) (pg. 4-6). Inherits from [tsplib95.models.StandardProblem](https://tsplib95.readthedocs.io/en/stable/pages/modules.html#tsplib95.models.StandardProblem).

The available specification fields are:
* `CAPACITY`
* `COMMENT`
* `DEMAND_DIMENSION`
* `DIMENSION`
* `DISPLAY_DATA_TYPE`
* `DISTANCE`
* `EDGE_DATA_FORMAT`
* `EDGE_WEIGHT_FORMAT`
* `EDGE_WEIGHT_TYPE`
* `NAME`
* `NODE_COORD_TYPE`
* `RISK_THRESHOLD`
* `SALESMEN`
* `SCALE`
* `SERVICE_TIME`
* `TYPE`
* `VEHICLES`

The available data fields are:
* `BACKHAUL_SECTION`
* `CTSP_SET_SECTION`
* `DEMAND_SECTION`
* `DEPOT_SECTION`
* `DISPLAY_DATA_SECTION`
* `DRAFT_LIMIT_SECTION`
* `EDGE_DATA_SECTION`
* `EDGE_WEIGHT_SECTION`
* `FIXED_EDGES_SECTION`
* `NODE_COORD_SECTION`
* `PICKUP_AND_DELIVERY_SECTION`
* `REQUIRED_NODES_SECTION`
* `SERVICE_TIME_SECTION`
* `TIME_WINDOW_SECTION`


You probably want to initialize a problem instance using one of the following class methods:

 #### _classmethod_ ```load(filepath, **options)```

 Load a problem instance from a text file.

 Inherited from [tsplib95.problems.Problem.load](https://tsplib95.readthedocs.io/en/stable/pages/modules.html#tsplib95.models.Problem.load).

 #### _classmethod_ ```parse(text, **options)```

 Parse text into a problem instance.

 Inherited from [tsplib95.problems.Problem.parse](https://tsplib95.readthedocs.io/en/stable/pages/modules.html#tsplib95.models.Problem.parse).

  #### _classmethod_ ```read(fp, **options)```

 Read a problem instance from a file-like object.

 Inherited from [tsplib95.problems.Problem.read](https://tsplib95.readthedocs.io/en/stable/pages/modules.html#tsplib95.models.Problem.read).

 ## Citation
 If you use PyLKH in your research, please cite it. You can generate an APA or BibTeX citation by clicking "Cite this repository" in the About section. Read more about citation files on GitHub [here](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files).
