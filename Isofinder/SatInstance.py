import os
import sys
from typing import List, Union
import itertools as it


class SatInstance:
    """
    A CNF where variables are symbols of {1, ..., n} for n > 0. Also allows a partial initialization of the assignment.

    Attributes:
        nb_variables (int): The exact number of variables of the instance
        clauses (List[List[int]]): A list of conjunctive clauses, where variables are either
        clauses_count (int): An upper bound on the number of clauses
        partial_assignment (List[Union[NoneType, bool]]): A list that represents a partial assignment of the variables
            of the instance, where partial_assignment[i] is, if not None, the value of variable i
    """

    nb_variables: int
    partial_assignment: List[int]
    simplified_variables_count: int
    clauses_count: int
    clauses: List[List[int]]
    simplified_clauses_count: int

    def __init__(self, nb_variables, nb_clauses):
        self.nb_variables = nb_variables
        self.partial_assignment = [None] * (nb_variables + 1)
        self.simplified_variables_count = 0

        self.clauses_count = 0
        self.clauses = [[] for _ in range(nb_clauses)]
        self.simplified_clauses_count = 0

        self.file = None

    def add_clause(self, variables: List[int]) -> None:
        """
        Add a clause that consists of a list of variables, assumed to be non-null signed integers.

        Args:
            variables (List[int]): A list of integers that represents the variables of the clause. If variable i is
                negated, then i should be negative
        """
        clause = variables[:]  # Create a copy as we will alter the clause

        # Simplify the formula : delete the clause when it is satisfied by the partial assignment, or remove the
        # literals that are false
        # Also assuming that no variable appears twice,
        for i, literal in enumerate(variables):
            if self.partial_assignment[abs(literal)] is not None:
                if literal > 0 and self.partial_assignment[abs(literal)] or \
                        literal < 0 and not self.partial_assignment[abs(literal)]:
                    self.simplified_clauses_count += 1
                    return
                clause[i] = 0

        clause = list(it.filterfalse(lambda x: x == 0, clause))
        self.simplified_variables_count += len(variables) - len(clause)

        if not clause:
            print("ERROR: Empty clause")  # No clause should be empty, by construction

        if self.file is not None:
            self.print_clause(clause, self.file)
        else:
            self.clauses[self.clauses_count] = clause

        self.clauses_count += 1

    def open_output_file(self, file_path: str):
        self.file = open(file_path, "w+")

        # Attempt to write an estimate of the numbers of variables and clauses
        self.file.write(f"p cnf {self.get_variables_count()} 0\n")

    def close_output_file(self):
        # Correction of the estimate of the numbers of variables and clauses
        self.file.seek(0, os.SEEK_SET)
        self.file.write(f"p cnf {self.get_variables_count()} {self.get_clauses_count()}\n")

        # Bad practice but only way I found to keep the SATInstance encapsulated
        self.file.close()

    def get_variables_count(self) -> int:
        return self.nb_variables

    def get_clauses_count(self) -> int:
        return self.clauses_count

    def get_clauses(self) -> int:
        for clause in self.clauses:
            yield clause

    def print_instance_data(self, file=sys.stdout) -> None:
        print(f"CNF with {self.get_variables_count()} variables and {self.get_clauses_count()} clauses", file=file)

    def print_clause(self, clause: list, file=sys.stdout) -> None:
        if isinstance(clause, list) and len(clause) > 0:
            file.write(' '.join(map(str, clause)))
            file.write(' 0\n')

    def print_instance(self, file=sys.stdout) -> None:
        """
        Print the SAT instance in CNF form, in the format usually used by SAT solvers like WalkSAT or MiniSAT, in the
        stream referenced by argument file

        Args:
            file: The output stream
        """
        file.write(f"p cnf {self.get_variables_count()} {self.get_clauses_count()}\n")
        for clause in self.clauses:
            if isinstance(clause, list) and len(clause) > 0:
                file.write(' '.join(map(str, clause)))
                file.write(' 0\n')
