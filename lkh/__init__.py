import os
import shutil
import subprocess
import tempfile
import warnings

from .problems import LKHProblem


def solve(solver='LKH', problem=None, **params):
    assert shutil.which(solver) is not None, f'{solver} not found.'
    assert ('problem_file' in params) ^ (problem is not None), 'Specify a problem object *or* a path.'

    if 'problem_file' in params:
        # annoying, but necessary to get the original problem dimension
        problem = LKHProblem.load(params['problem_file'])

    if not isinstance(problem, LKHProblem):
        warnings.warn('Subclassing LKHProblem is recommended. Proceed at your own risk!')

    if len(problem.depots) > 1:
        warnings.warn('LKH-3 cannot solve multi-depot problems.')

    prob_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    problem.write(prob_file)
    prob_file.write('\n')
    prob_file.close()
    params['problem_file'] = prob_file.name

    if 'tour_file' not in params:
        tour_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        params['tour_file'] = tour_file.name
        tour_file.close()

    par_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
    par_file.write('SPECIAL\n')
    for k, v in params.items():
        par_file.write(f'{k.upper()} = {v}\n')
    par_file.close()

    try:
        # stdin=DEVNULL for preventing a "Press any key" pause at the end of execution
        subprocess.check_output([solver, par_file.name], stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        raise Exception(e.output.decode())

    # the tour file produced by LKH-3 includes dummy nodes to indicate depots
    # for example, if a problem has DIMENSION=32 (1 depot node + 31 task nodes),
    # the tour file will have a SINGLE tour with DIMENSION=36 (5 depot nodes + 31 task nodes)
    solution = LKHProblem.load(params['tour_file'])
    tour = solution.tours[0]
    # convert this tour to multiple routes
    routes = []
    route = []
    for node in tour:
        if node in problem.depots or node > problem.dimension:
            if len(route) > 0:
                routes.append(route)
            route = []
        else:
            route.append(node)
    routes.append(route)

    os.remove(par_file.name)
    if 'prob_file' in locals():
        os.remove(prob_file.name)
    if 'tour_file' in locals():
        os.remove(tour_file.name)

    return routes
