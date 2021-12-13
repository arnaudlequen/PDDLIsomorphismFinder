import os
import itertools as it
import math
import sys
from typing import List, Union


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
    partial_assignment: List[bool]
    simplified_variables_count: int
    clauses_count: int
    clauses: List[List[int]]
    simplified_clauses_count: int

    clause_padding = 20  # Padding for the

    def __init__(self, nb_variables, clause_estimation=1e20):
        self.nb_variables = nb_variables
        self.partial_assignment = [None] * (nb_variables + 1)

        self.clauses_count = 0
        self.clauses = []
        self.clause_padding = math.ceil(math.log10(clause_estimation + 1))
        # self.clauses = [[] for _ in range(nb_clauses)]

        # Statistics
        self.simplified_variables_count = 0
        self.last_simplified_variables_count = 0
        self.simplified_clauses_count = 0
        self.last_simplified_clauses_count = 0
        self.new_clauses_count = 0

        self.file = None

    def add_clause(self, variables: List[int]) -> bool:
        """
        Add a clause that consists of a list of variables, assumed to be non-null signed integers.

        Args:
            variables (List[int]): A list of integers that represents the variables of the clause. If variable i is
                negated, then i should be negative
        """
        if not variables:
            return True

        # Create a copy as we will alter the clause
        # Maybe there is no need to?
        clause = variables[:]

        # Simplify the formula : delete the clause when it is satisfied by the partial assignment, or remove the
        # literals that are false
        # Also assuming that no variable appears twice,
        for i, literal in enumerate(variables):
            if self.partial_assignment[abs(literal)] is not None:
                if literal > 0 and self.partial_assignment[abs(literal)] or \
                        literal < 0 and not self.partial_assignment[abs(literal)]:
                    self.simplified_clauses_count += 1
                    return True
                clause[i] = 0

        clause = list(it.filterfalse(lambda x: x == 0, clause))
        self.simplified_variables_count += len(variables) - len(clause)

        if not clause:
            return False
            # print("ERROR: Empty clause")

        if self.file is not None:
            self.print_clause(clause, self.file)
        else:
            self.clauses.append(clause)

        self.new_clauses_count += 1
        self.clauses_count += 1

        return True

    def open_output_file(self, file_path: str):
        self.file = open(file_path, "w+")

        # Attempt to write an estimate of the numbers of variables and clauses
        # The padding on the number of clauses is necessary in order not to have to rewrite the whole file on file
        # after the correction
        self.file.write(f"p cnf {self.get_variables_count()} {'0'*self.clause_padding}\n")

    def close_output_file(self):
        # Correction of the estimate of the numbers of variables and clauses
        self.file.seek(0, os.SEEK_SET)
        self.file.write(f"p cnf {self.get_variables_count()} {self.get_clauses_count():0>{self.clause_padding}}\n")

        # Bad practice but only way I found to keep the SATInstance encapsulated
        self.file.close()

    def set_partial_assignment(self, partial_assignment: List[bool]):
        self.partial_assignment = partial_assignment

    def get_new_clauses_count(self) -> int:
        """
        Return the number of clauses that were added in the instance since the last call to this function, or the
        creation of the instance if this function has never been called before
        """
        new_clauses_count = self.new_clauses_count
        self.new_clauses_count = 0

        return new_clauses_count

    def get_new_simplified_clauses_count(self) -> int:
        """
        Return the number of clauses that were simplified since the last call of this function, or the creation of the
        instance if this function has never been called before
        """
        new_clauses_count = self.simplified_clauses_count - self.last_simplified_clauses_count
        self.last_simplified_clauses_count = self.simplified_clauses_count

        return new_clauses_count

    def get_simplified_variables_count(self) -> int:
        return self.simplified_variables_count

    def get_simplified_clauses_count(self) -> int:
        return self.simplified_clauses_count

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
