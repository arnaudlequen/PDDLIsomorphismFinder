import sys
import itertools as it

class SatInstance:
    def __init__(self, nbVariables, nbClauses):
        # Fix this: variableCount is the current count, while clausesCount is just a pointer
        self.variableCount = nbVariables

        self.clausesCount = 0
        self.clauses = [None]*nbClauses

    def addClause(self, variables):
        """
        Add a clause that consists of a list of variables, assumed to be non-null signed integers
        """
        #assert list(it.filterfalse(lambda x: isinstance(x, int) and x != 0, variables)) == [], "Invalid clause: variables must be non-null integers"
        #self.variableCount = max(self.variableCount, max(list(map(abs, variables))))
        self.clauses[self.clausesCount] = variables
        self.clausesCount += 1

    def getVariablesCount(self):
        return self.variableCount

    def getClausesCount(self):
        return self.clausesCount

    def getClauses(self):
        for clause in self.clauses:
            yield clause

    def printInstanceData(self, file=sys.stdout):
        print(f"CNF with {self.getVariablesCount()} variables and {self.getClausesCount()} clauses", file=file)

    def printInstance(self, file=sys.stdout):
        """
        Print the SAT instance in CNF form, in the format usually used by SAT solvers like WalkSAT or MiniSAT, in the
        stream referenced by argument file

        Args:
            file: The output stream
        """
        file.write(f"p cnf {self.getVariablesCount()} {self.getClausesCount()}\n")
        for clause in self.clauses:
            if isinstance(clause, list) and len(clause) > 0:
                file.write(' '.join(map(str, clause)))
                file.write(' 0\n')
