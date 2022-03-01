# Summary
Python script that finds isormophisms of subinstances between classical planning problems.
The algorithm is based on a compilation of the problem to a CNF, that is passed to a SAT solver.
It is aided by a constraint-propagation-based preprocessing, which greatly improves its efficiency.

# Installation
Tested with Ubuntu 20.04. First, compile the SAT solver and the parsers using:
```shell
make
```
Then create a Python virtual environment, and install the dependencies. For instance,
```shell
python3 -m venv env
source ./env/bin/activate
python3 -m pip install -r requirements.txt
```

# Usage
All commands below should be run within the virtual environment created in the section above,
and at the root of the directory
```shell
python3 main.py [-h] [-c CNFPATH] [-s SATSOLVER] [-o OUTPUT] [-t TRACE]
               [--touist | --no-touist] [--clean | --no-clean | -l]
               [--cp | --no-cp]
               domainbig.pddl instancebig.pddl domainsmall.pddl
               instancesmall.pddl
```

### Positional arguments:

  **domainbig.pddl**: The domain file in PDDL format

  **instancebig.pddl**: The file of the problem from which to extract a
                        subproblem, in PDDL format

  **domainsmall.pddl**: The domain file in PDDL format

  **instancesmall.pddl**: The file of the subproblem to extract, in PDDL format

Optional arguments:
  **-h, --help**: Show this help message and exit

  **-c CNFPATH, --cnfpath CNFPATH**: 
                        The file in which to save the SAT formula that is
                        passed to the solver

  **-s SATSOLVER, --satsolver SATSOLVER**: 
                        The SAT solver to use

  **-o OUTPUT, --output OUTPUT**:
                        The file in which to save the sub-isomorphism

  **-t TRACE, --trace TRACE**:
                        Output a datafile that summarizes the main data points
                        of the execution

  **--touist, --no-touist**:
                        Use TouISTPlan to extract STRIPS problems from PDDL
                        files (default: True)

  **--clean, --no-clean, -l**:
                        Do not show progress bars and create a clean trace for
                        further processing (default: False)

  **--cp, --no-cp**:         Run constraint propagation preprocessing (default:
                        True)

# Test sets
In order to run tests on whole domains, scripts in folder Tests can be used as follows:
```shell
cd ./Tests
bash general.sh domain imin imax
```
where `domain` is the name of the domain in the Benchmarks folder (ex. blocks, barman, etc.),
and `imin` and `imax` are respectively the smallest and biggest id of the instances to test.

For instance, to test instances `pfile4.pddl` to `pfile10.pddl` of domain `blocks` against each other,

```shell
bash general.sh blocks 4 10
```

Script `general_nocp.sh` works in a similar way, but will not use the constraint-propagation step.

# Supports
PDDL planning problems with propositional preconditions and effects

# Requirements
- Python 3.10
- Python venv
- Opam
- Make
