import argparse
import os
import sys
from SubisoFinder import *
from StripsConverter import *
from SatInstance import *
import subprocess
from time import time

def main(argv):

    parser = argparse.ArgumentParser(description="Sub-isomorphism finder for STRIPS planning problems")
    parser.add_argument('domainPath', metavar='domain.pddl', type=str, help="The domain file in PDDL format")
    parser.add_argument('instance1Path', metavar='instancebig.pddl', type=str, \
                        help="The file of the problem from which to extract a subproblem, in PDDL format")
    parser.add_argument('instance2Path', metavar='instancesmall.pddl', type=str, \
                        help="The file of the subproblem to extract, in PDDL format")
    parser.add_argument('-c', '--cnfpath', type=str, default='./tmp/satencoding.cnf', \
                        help="The file in which to save the SAT formula that is passed to the solver")
    parser.add_argument('-s', '--satsolver', type=str, default='./Solvers/Bin/glucose-syrup_static', \
                        help="The path to the SAT solver binary")
    parser.add_argument('-o', '--output', type=str, default='output.isom', \
                        help="The file in which to save the sub-isomorphism")
    args = parser.parse_args()

    filler = ''.join(['=']*30)

    try:
        os.mkdir('./tmp')
    except FileExistsError:
        pass

    global_start_time = time()
    # Extract problems from file
    #domainPath, instance1Path, instance2Path = argv[1:4]

    step_start = time()
    print("Extracting domain and instances from file...")
    print(filler)
    converter = StripsConverter()
    print(args)
    pddlDomain = converter.buildDomain(args.domainPath)
    pddlInstance1 = converter.buildInstance(args.instance1Path)
    pddlInstance2 = converter.buildInstance(args.instance2Path)
    print(f"PDDL extraction done in {time() - step_start:.1f}s!\n")

    # Convert them to STRIPS
    step_start = time()
    print("Converting problems to STRIPS...")
    print(filler)
    problem1 = converter.buildStripsProblem(pddlDomain, pddlInstance1)
    problem2 = converter.buildStripsProblem(pddlDomain, pddlInstance2)
    print(f"Conversion to STRIPS done in {time() - step_start:.1f}s!\n")

    # Translation to SAT
    step_start = time()
    print("Translating the STRIPS-sub-isomorphism instance to SAT...")
    print(filler)
    subisoFinder = SubisoFinder()
    satInstance = subisoFinder.convertToSAT(problem1, problem2)
    print(f"Translation done in {time() - step_start:.1f}s!\n")

    # Save the partial results
    step_start = time()
    print("Saving the results...")
    print(filler)
    satFormulaPath = args.cnfpath
    file = open(satFormulaPath, 'w+')
    satInstance.printInstance(file)
    file.close()
    print(f"Saving done in {time() - step_start:.1f}s!")
    print(f"Saved the result in file {satFormulaPath}\n")

    # Interpret the results
    # Use a subprocess to run something as a backend (I need to pass a file, as it seems)
    # The output of the solver being in the commandline, I need to read the stdout of the process
    start_time = time()
    print(f"Calling the SAT solver in a subprocess...")
    print(filler)
    solverPath = args.satsolver
    # Added option -model for Glucose
    process = subprocess.run([solverPath, '-model', satFormulaPath], capture_output=True, text=True)
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

        if outcome != None:
            if line_elements[0] == 'v':
                assignment = [(False if var[0] == '-' else True) for var in line_elements]
                # The first text character is v, which is not part of the variable assigment. Variables are however
                # numbered starting from 1, so this is convenient
                assignment[0] = None
                break

    print(f"Isomorphism: {'FOUND' if outcome else 'NOT FOUND'}")
    print(f"SAT solving done in {time() - step_start:.1f}s!\n")
    if outcome:
        print("Building the isomorphism...")
        print(filler)
        isoPath = args.output
        isoFile = open(isoPath, 'w+')

        subisoFinder.interpretAssignment(problem1, problem2, assignment, isoFile)

        isoFile.close()
        print("Isomorphism built")
        print(f"Saved the result in file {isoPath}\n")

    print(filler)
    print(f"Total time: {time() - global_start_time:.1f}s")
    print()


if __name__ == '__main__':
    main(sys.argv)
