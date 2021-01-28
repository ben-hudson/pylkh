import tsplib95 as tsplib
import tempfile
import subprocess
import shutil

def solve(solver='LKH', problem=None, **params):
    assert shutil.which(solver) is not None, f'{solver} not found.'

    valid_problem = problem is not None and isinstance(problem, tsplib.models.StandardProblem)
    assert ('problem_file' in params) ^ valid_problem, 'Specify a TSPLIB95 problem object or a path.'
    if problem is not None:
        # hack for bug in tsplib
        problem.depots = map(lambda x: f'{x}\n', problem.depots)

        prob_file = tempfile.NamedTemporaryFile(mode='w')
        problem.write(prob_file)
        prob_file.flush()
        params['problem_file'] = prob_file.name

    if 'sintef_solution_file' not in params:
        sol_file = tempfile.NamedTemporaryFile(mode='w')
        params['sintef_solution_file'] = sol_file.name

    with tempfile.NamedTemporaryFile(mode='w') as par_file:
        par_file.write('SPECIAL\n')
        for k, v in params.items():
            par_file.write(f'{k.upper()} = {v}\n')
        par_file.flush()

        ret = subprocess.run([solver, par_file.name], check=True)

        # iterate over solution
        sol_iter = iter(open(params['sintef_solution_file'], 'r'))
        sol_line = next(sol_iter)
        while not 'Solution' in sol_line:
            sol_line = next(sol_iter)

        routes = []
        for line in sol_iter:
            route_name, route_stops = line.split(':')
            route = list(map(int, route_stops.strip().split(' ')))
            routes.append(route)

        return routes
