import argparse
import os
import sys
from SubisoFinder import *
from StripsConverter import *
from SatInstance import *
import subprocess
from time import perf_counter

filler = ''.join(['='] * 30)
small_filler = ''.join(['-'] * 30)


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main(argv):
    parser = argparse.ArgumentParser(description="Sub-isomorphism finder for STRIPS planning problems")
    parser.add_argument('domain1Path', metavar='domainbig.pddl', type=str, help="The domain file in PDDL format")
    parser.add_argument('instance1Path', metavar='instancebig.pddl', type=str,
                        help="The file of the problem from which to extract a subproblem, in PDDL format")
    parser.add_argument('domain2Path', metavar='domainsmall.pddl', type=str, help="The domain file in PDDL format")
    parser.add_argument('instance2Path', metavar='instancesmall.pddl', type=str,
                        help="The file of the subproblem to extract, in PDDL format")
    parser.add_argument('-c', '--cnfpath', type=str, default='./tmp/satencoding.cnf',
                        help="The file in which to save the SAT formula that is passed to the solver")
    parser.add_argument('-s', '--satsolver', type=str, default='./Solvers/Bin/glucose-syrup_static',
                        help="The path to the SAT solver binary")
    parser.add_argument('-o', '--output', type=str, default='output.isom',
                        help="The file in which to save the sub-isomorphism")
    parser.add_argument('-t', '--trace', type=str, default=None,
                        help="Output a datafile that summarizes the main data points of the execution")
    parser.add_argument('--touist', type=str2bool, nargs='?', const=True, default=False,
                        help="Use TouISTPlan to extract STRIPS problems from PDDL files")
    args = parser.parse_args()

    try:
        os.mkdir('./tmp')
    except FileExistsError:
        pass

    try:
        os.mkdir('./solvedata')
    except FileExistsError:
        pass

    steps_duration = {}
    global_start_time = perf_counter()

    print(filler)
    print("STRIPS Isomorphism finder")
    print(filler)
    print()

    problem1, problem2 = None, None
    if args.touist:
        problem1, problem2 = touistplan_parser(args, steps_duration)
    else:
        problem1, problem2 = adhoc_parser(args, steps_duration)

    # Translation to SAT
    step_start = perf_counter()
    print("Translating the STRIPS-sub-isomorphism instance to SAT...")
    print(filler)
    subiso_finder = SubisoFinder()
    sat_instance = subiso_finder.convert_to_sat(problem1, problem2, args.cnfpath)
    if sat_instance is None:
        return
    step_time = perf_counter() - step_start
    print(f"Translation done in {step_time:.1f}s!\n")
    print(f"Saved result in file {args.cnfpath}\n")
    steps_duration["sat_translation"] = step_time

    # Interpret the results
    step_start = perf_counter()
    print(f"Calling the SAT solver in a subprocess...")
    print(filler)
    solver_path = args.satsolver
    # Added option -model for Glucose
    process = subprocess.run([solver_path, '-model', args.cnfpath], capture_output=True, text=True)
    print("SAT solving done. Processing the output...")

    outcome = None
    assignment = None

    # I'm copying the output and transforming it, so it's not super efficient
    for line in process.stdout.split('\n'):
        if len(line) == 0:
            continue
        line_elements = line.split()

        if 's' in line_elements:
            if 'SATISFIABLE' in line_elements:
                outcome = True
            else:
                outcome = False
                continue

        if outcome is not None:
            if line_elements[0] == 'v':
                assignment = [(False if var[0] == '-' else True) for var in line_elements]
                # The first text character is v, which is not part of the variable assigment. Variables are however
                # numbered starting from 1, so this is convenient
                assignment[0] = None
                break

    print(f"Isomorphism: {'FOUND' if outcome else 'NOT FOUND'}")
    step_time = perf_counter() - step_start
    print(f"SAT solving done in {step_time:.1f}s!\n")
    steps_duration["sat_solving"] = step_time
    if outcome:
        print("Building the isomorphism...")
        print(filler)
        iso_path = args.output

        with open(iso_path, 'w+') as iso_file:
            subiso_finder.interpret_assignment(problem1, problem2, assignment, iso_file)

        print("Isomorphism built")
        print(f"Saved the result in file {iso_path}\n")

    print(filler)
    step_time = perf_counter() - global_start_time
    print(f"Total time: {step_time:.1f}s")
    steps_duration["total_time"] = step_time
    if args.trace is not None:
        print(f"Saving trace in {args.trace}")
        with open(args.trace, "w+") as file:
            ordered_times = [(k, v) for k, v in steps_duration.items()]
            file.write(f"variables,clauses,simplified_variables,simplified_clauses,")
            file.write(','.join(map(lambda x: x[0], ordered_times)))
            file.write(f"\n")
            file.write(f"{sat_instance.get_variables_count()},"
                       f"{sat_instance.get_clauses_count()},"
                       f"{sat_instance.get_simplified_variables_count()},"
                       f"{sat_instance.get_simplified_clauses_count()},")
            file.write(','.join(map(lambda x: f'{x[1]:0.1f}', ordered_times)))
    print()


def touistplan_parser(args, steps_duration):
    blankfile = open('./tmp/blankrules.touistl', 'w+')
    blankfile.close()

    # Running the process writes in a file that is then read during a call to touist_process_problem_sets
    parsing_start = perf_counter()

    print("Parsing problem 1...")
    step_start = perf_counter()
    print(small_filler)
    problem1 = touistplan_parse_single(args.domain1Path, args.instance1Path)
    print(f"Done. Found {problem1.get_fluent_count()} fluents and {problem1.get_operator_count()} operators "
          f"in {perf_counter() - step_start:.2f}s")
    print()

    print("Parsing problem 2...")
    print(small_filler)
    problem2 = touistplan_parse_single(args.domain2Path, args.instance2Path)
    print(f"Done. Found {problem2.get_fluent_count()} fluents and {problem2.get_operator_count()} operators "
          f"in {perf_counter() - step_start:.2f}s")
    print()

    return problem1, problem2


def trim_action_or_predicate(element):
    return element[2:]


def touistplan_parse_single(domain_path, instance_path):
    step_start = perf_counter()
    print("Calling TouISTPlan to extract STRIPS problem 1 from file...")
    subprocess_args = ['./Solvers/touistplan', domain_path, instance_path, '-e', 'sat',
                       '-insat', './tmp/blankrules.touistl']
    process = subprocess.run(subprocess_args, capture_output=True)
    print(f"Extraction done in {perf_counter() - step_start:.1f}s")
    step_start = perf_counter()
    print("Processing the output files...")
    problem = touist_process_problem_sets()
    print(f"Processing done in {perf_counter() - step_start:.1f}s")

    return problem


def touist_process_problem_sets() -> StripsProblem:
    predicate_to_varId = {}
    varId_to_predicate = {}

    action_to_opId = {}
    opId_to_action = {}
    opId_to_operator = {}

    # Temporary variables as we need to store the predicates before they are assigned an id, if we want to perform a
    # single pass
    init_pos_predicates = []
    goal_pos_predicates = []

    init_pos = []
    init_neg = []
    goal_pos = []
    goal_neg = []

    with open('./solvedata/in.sets.txt', 'r') as sets_file:
        line = sets_file.readline()
        while line:
            if line.startswith("$t_"):
                line = sets_file.readline()
                continue

            if line.startswith("$F ="):
                predicates = line.split('[')[1][:-2].split(',')
                predicates = map(trim_action_or_predicate, predicates)
                for varId, predicate in enumerate(predicates):
                    predicate_to_varId[predicate] = varId
                    varId_to_predicate[varId] = predicate

            elif line.startswith("$O ="):
                actions = line.split('[')[1][:-2].split(',')
                actions = map(trim_action_or_predicate, actions)
                for opId, action in enumerate(actions):
                    action_to_opId[action] = opId
                    opId_to_action[opId] = action

                    operator_name = action.split('_')[1]
                    operator = Operator(operator_name, [], [], [], [])
                    opId_to_operator[opId] = operator

            # Todo: refactor this whole block
            elif line.startswith("$Cond("):
                action, predicates = line.split(' = ')
                action = trim_action_or_predicate(action[6:-1])
                predicates = list(map(trim_action_or_predicate, predicates[1:-2].split(',')))

                opId = action_to_opId[action]
                operator = opId_to_operator[opId]
                operator.pre_pos = list(map(lambda predicate: predicate_to_varId[predicate], predicates))

            elif line.startswith("$Add("):
                action, predicates = line.split(' = ')
                action = trim_action_or_predicate(action[5:-1])
                predicates = list(map(trim_action_or_predicate, predicates[1:-2].split(',')))

                opId = action_to_opId[action]
                operator = opId_to_operator[opId]
                operator.eff_pos = list(map(lambda predicate: predicate_to_varId[predicate], predicates))

            elif line.startswith("$Del("):
                action, predicates = line.split(' = ')
                action = trim_action_or_predicate(action[5:-1])
                predicates = list(map(trim_action_or_predicate, predicates[1:-2].split(',')))

                opId = action_to_opId[action]
                operator = opId_to_operator[opId]
                operator.eff_neg = list(map(lambda predicate: predicate_to_varId[predicate], predicates))

            elif line.startswith("$I = "):
                _, predicates = line.split(' = ')
                init_pos_predicates = list(map(trim_action_or_predicate, predicates[1:-2].split(',')))

            elif line.startswith("$G = "):
                _, predicates = line.split(' = ')
                goal_pos_predicates = list(map(trim_action_or_predicate, predicates[1:-2].split(',')))

            line = sets_file.readline()

        init_pos = list(map(lambda p: predicate_to_varId[p], init_pos_predicates))
        goal_pos = list(map(lambda p: predicate_to_varId[p], goal_pos_predicates))

        problem = StripsProblem(predicate_to_varId, varId_to_predicate,
                                action_to_opId, opId_to_action, opId_to_operator,
                                init_pos, init_neg,
                                goal_pos, goal_neg)

        return problem


def adhoc_parser(args, steps_duration):
    """
    Extract STRIPS instances out of PDDL files and return STRIPSProblem instances
    """
    # Extract problems from file
    step_start = perf_counter()
    print("Extracting domain and instances from file...")
    print(filler)
    converter = StripsConverter()
    pddl_domain1 = converter.build_domain(args.domain1Path)
    pddl_domain2 = converter.build_domain(args.domain2Path)
    pddl_instance1 = converter.build_instance(args.instance1Path)
    pddl_instance2 = converter.build_instance(args.instance2Path)
    step_time = perf_counter() - step_start
    print(f"PDDL extraction done in {step_time:.1f}s!\n")
    steps_duration["pddl_extraction"] = step_time

    # Convert them to STRIPS
    step_start = perf_counter()
    print("Converting problems to STRIPS...")
    print(filler)
    problem1 = converter.build_strips_problem(pddl_domain1, pddl_instance1)
    problem2 = converter.build_strips_problem(pddl_domain2, pddl_instance2)
    step_time = perf_counter() - step_start
    print(f"Conversion to STRIPS done in {step_time:.1f}s!\n")
    steps_duration["grounding"] = step_time

    return problem1, problem2


if __name__ == '__main__':
    main(sys.argv)
