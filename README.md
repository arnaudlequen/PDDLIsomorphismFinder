# Summary
Python script that finds (sub-)isomorphisms between classical planning problems. Currently only supports sub-isomorphisms.
The script translates the problem to a CNF that is then passed to a SAT solver.

# Installation
Please compile any of the SAT solvers present in the `Solvers/Source` folder, and put the resulting file in `Solvers/Bin`

# Usage
`python main.py [-h] [-c CNFPATH] [-s SATSOLVER] [-o OUTPUT]
               domain.pddl instancebig.pddl instancesmall.pddl`

Positional arguments:
- domain.pddl: The domain file in PDDL format
- instancebig.pddl: The file of the problem from which to extract a subproblem, in PDDL format
- instancesmall.pddl: The file of the subproblem to extract, in PDDL format

Optional arguments:
- -h, --help: Show an help message
- -c CNFPATH, --cnfpath CNFPATH: The file in which to save the SAT formula that is passed to the solver

- -s SATSOLVER, --satsolver SATSOLVER: The path to the SAT solver binary
- -o OUTPUT, --output OUTPUT: The file in which to save the sub-isomorphism

# Supports
STRIPS domains with propositional preconditions and effects

# Requirements
- Python 3.9
- Antlr 4.9.2
- Python packages: attrs
- Python runtime for Antlr. Download with `pip install antlr4-python3-runtime`
