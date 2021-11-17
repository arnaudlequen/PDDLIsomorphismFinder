import sys
from typing import List, Union


class SatInstance:
    """
    A CNF where variables are symbols of {1, ..., n} for n > 0. Also allows a partial initialization of the assignment.

    Attributes:
        nb_variables (int): The exact number of variables of the instance
        clauses (List)
    """
    clauses: List[Union[type(None), bool]]

    def __init__(self, nb_variables, nb_clauses):
        self.nb_variables: int = nb_variables

        self.clauses: List[List[Union[type(None), int]]] = [None] * nb_clauses
        self.clauses_count: int = 0

    def add_clause(self, variables: List[int]) -> None:
        """
        Add a clause that consists of a list of variables, assumed to be non-null signed integers.

        Args:
            variables (List[int]): A list of integers that represents the variables of the clause
        """
        # assert list(it.filterfalse(lambda x: isinstance(x, int) and x != 0, variables)) == [], "Invalid clause: variables must be non-null integers"
        # self.variable_count = max(self.variable_count, max(list(map(abs, variables))))
        self.clauses[self.clauses_count] = variables
        self.clauses_count += 1

    def get_variables_count(self) -> int:
        return self.nb_variables

    def get_clauses_count(self) -> int:
        return self.clauses_count

    def get_clauses(self) -> int:
        for clause in self.clauses:
            yield clause

    def print_instance_data(self, file=sys.stdout) -> None:
        print(f"CNF with {self.get_variables_count()} variables and {self.get_clauses_count()} clauses", file=file)

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
