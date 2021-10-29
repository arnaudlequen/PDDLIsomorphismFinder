# Summary
Python script that finds (sub-)isomorphisms between classical planning problems. Currently only supports sub-isomorphisms.

# Usage
`python ./Isofinder/main.py [domain.pdd] [instance_big.pddl] [instance_small.pddl] [SAT_formula_output_path.cnf] [solver] [isomorphism_output_path]`

# Supports
STRIPS domains with propositional preconditions and effects

# Requirements
- Python 3.9
- Antlr 4.9.2
- Python runtime for Antlr. Download with `pip install antlr4-python3-runtime`
