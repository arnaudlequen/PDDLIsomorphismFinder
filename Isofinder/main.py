import sys
from SubisoFinder import *
from StripsConverter import *
from SatInstance import *
from time import time
import subprocess

def main(argv):

    if len(argv) < 7:
        print("Usage: python main.py domain.pddl instancebig.pddl instancesmall.pddl satFormulaPath solverPath isoPath")
        return

    filler = ''.join(['=']*30)

    global_start_time = time()
    # Extract problems from file
    domainPath, instance1Path, instance2Path = argv[1:4]

    step_start = time()
    print("Extracting domain and instances from file...")
    print(filler)
    converter = StripsConverter()
    pddlDomain = converter.buildDomain(domainPath)
    pddlInstance1 = converter.buildInstance(instance1Path)
    pddlInstance2 = converter.buildInstance(instance2Path)
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
    satFormulaPath = argv[4]
    file = open(satFormulaPath, 'w+')
    satInstance.printInstance(file)
    file.close()
    print(f"Saving duration: {time() - step_start:.1f}s")
    print(filler)
    print(f"Saved the result in file {satFormulaPath}\n")

    # Interpret the results
    # Use a subprocess to run something as a backend (I need to pass a file, as it seems)
    # The output of the solver being in the commandline, I need to read the stdout of the process
    print(f"Calling the SAT solver in a subprocess...")
    print(filler)
    solverPath = argv[5]
    process = subprocess.run([solverPath, satFormulaPath], capture_output=True, text=True)
    print("SAT solving done. Processing the output...")

    outcome = None
    assignment = None

    # I'm copying the output and transforming it, so it's not super efficient
    for line in process.stdout.split('\n'):
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
    print("Building the isomorphism...")
    isoPath = argv[6]
    isoFile = open(isoPath, 'w+')

    #
    # Utiliser une fonction de la classe StripsSubIsoFinder
    # Passer le stream dans lequel écrire l'isomorphisme
    #


    subisoFinder.interpretAssignment(problem1, problem2, assignment, isoFile)


    isoFile.close()
    print("Isomorphism built")
    print(f"Saved the result in file {isoPath}\n")

    print(filler)
    print(f"Total time: {time() - global_start_time:.1f}")
    print()


if __name__ == '__main__':
    main(sys.argv)
