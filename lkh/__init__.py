import tsplib95 as tsplib
import tempfile
import subprocess
import shutil

def solve(solver='LKH', problem=None, quiet=False, **params):
    assert shutil.which(solver) is not None, f'{solver} not found.'

    valid_problem = problem is not None and isinstance(problem, tsplib.models.StandardProblem)
    assert ('problem_file' in params) ^ valid_problem, 'Specify a TSPLIB95 problem object *or* a path.'
    if problem is not None:
        # hack for bug in tsplib
        if len(problem.depots) > 0:
            problem.depots = map(lambda x: f'{x}\n', problem.depots)

        prob_file = tempfile.NamedTemporaryFile(mode='w')
        problem.write(prob_file)
        prob_file.flush()
        params['problem_file'] = prob_file.name

    # need dimension of problem to parse solution
    problem = tsplib.load(params['problem_file'])

    if 'tour_file' not in params:
        tour_file = tempfile.NamedTemporaryFile(mode='w')
        params['tour_file'] = tour_file.name

    with tempfile.NamedTemporaryFile(mode='w') as par_file:
        par_file.write('SPECIAL\n')
        for k, v in params.items():
            par_file.write(f'{k.upper()} = {v}\n')
        par_file.flush()

        stdout = subprocess.DEVNULL if quiet else subprocess.STDOUT
        stderr = subprocess.STDOUT
        ret = subprocess.run([solver, par_file.name], stdout=stdout, stderr=stderr, check=True)

        # iterate over solution
        with open(params['tour_file'], 'r') as tour:
            # skip header
            line = next(tour)
            while 'TOUR_SECTION' not in line:
                line = next(tour)

            routes = []
            route = []

            line = next(tour)
            while '-1' not in line:
                node = int(line)
                if node > problem.dimension:
                    routes.append(route)
                    route = []
                elif node not in problem.depots:
                    route.append(node)

                line = next(tour)

            routes.append(route)

            return routes
