import lkh
import pathlib
import pytest
import random
import tarfile
import warnings

misformatted_instances = [
    '**/burma14.tsp',
    '**/E-n33-k4.vrp',
    'ACVRP/INSTANCES/*',
    'CTSP/INSTANCES/H/usa13509-10.ctsp',
    'k-TSP/INSTANCES/TSPLIB/*',
    'MLP/INSTANCES/TSPLIB/dsj1000ceil.mlp',
    'mTSP/INSTANCES/TSP/dsj1000.tsp',
    'STTSP/INSTANCES/*',
    'TSPTW/INSTANCES/Silva/*',
    'VRPSPD/INSTANCES/D/CON3-0.vrpspd',
]

# helper to find instance files in tarball
def find_instances(tarball):
    for member in tarball:
        if member.isfile():
            path = pathlib.PurePath(member.name)
            if 'INSTANCES' in str(path) \
                and not any(path.match(p) for p in misformatted_instances) \
                and path.suffix != '':
                yield member.name

instances_paths = list(pathlib.Path('tests/test_instances').rglob('*.tgz'))
instance_types=[p.stem for p in instances_paths]

@pytest.mark.parametrize("instances_path", instances_paths, ids=instance_types)
def test_parse(instances_path):
    with tarfile.open(instances_path) as tarball:
        for instance_path in find_instances(tarball):
            instance_file = tarball.extractfile(instance_path)
            problem = lkh.LKHProblem.parse(instance_file.read().decode('ascii'))
            print(problem.render())

@pytest.mark.parametrize("instances_path", instances_paths, ids=instance_types)
def test_solve(instances_path):
    with tarfile.open(instances_path) as tarball:
        instance_paths = list(find_instances(tarball))
        if len(instance_paths) > 0:
            instance_file = tarball.extractfile(random.choice(instance_paths))
            problem = lkh.LKHProblem.parse(instance_file.read().decode('ascii'))
            try:
                lkh.solve(problem=problem, runs=10, max_trials=100)
            except lkh.NoToursException as e:
                warnings.warn(e)

if __name__ == '__main__':
    pytest.main()
