import os
import shutil
import subprocess
import tempfile

import tsplib95 as tsplib

from .problems import LKHProblem


def solve(solver='LKH', problem=None, **params):
    assert shutil.which(solver) is not None, f'{solver} not found.'

    valid_problem = problem is not None and isinstance(problem, tsplib.models.StandardProblem)
    assert ('problem_file' in params) ^ valid_problem, 'Specify a problem object *or* a path.'
    if problem is not None:
        # fix for https://github.com/rhgrant10/tsplib95/pull/16
        if len(problem.depots) > 0 and not isinstance(problem, LKHProblem):
            problem.depots = map(lambda x: f'{x}\n', problem.depots)

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

    solution = tsplib.load(params['tour_file'])

    os.remove(par_file.name)
    if 'prob_file' in locals():
        os.remove(prob_file.name)
    if 'tour_file' in locals():
        os.remove(tour_file.name)

    return solution.tours
