from DomainListener import *
from InstanceListener import *
from StripsConverter import *
from SatInstance import *
from Utils import progressBar

class SubisoFinder():
    def __init__(self):
        self.verboseActionNames = True

        self.steps = [
        'FluentsImages',
        'OperatorsImages',
        'MorphismProperty',
        'BijectionProperty',
        'OperatorsInjectivity',
        #'InitialStateConservation',
        #'GoalStateConservation',
        ]

    def convertToSAT(self, problem1, problem2):
        """
        Consider the problem STRIPS-subproblem-isomorphism(problem1, problem2), where one tries to find a subproblem of
        problem1 that is isomorphic to problem2. This function gives a SAT encoding of it

        Args:
            problem1: The problem from which to find a subproblem that is isomorphic to problem2. An instance of StripsProblem
            problem2: The smaller problem
        """
        n1, m1 = problem1.getFluentCount(), problem1.getOperatorCount()
        n2, m2 = problem2.getFluentCount(), problem2.getOperatorCount()

        if n1 < n2 or m1 < m2:
            print("The target problem is too big, no subproblem exists")
            return None

        # Functions that help with the conversion from the problem's data to variables of the SAT formula
        fToFId, fIdToF, oToOId, oIdToO = self.getObjectsToIdFunctions(problem1, problem2)

        # Definition of the formula
        expectedClauseCount = n2 + n2*(n1**2) + m2 + m2*(m1**2) + 4*m2*m1*n2 + m1*(m2**2) + 2*n1 + 2*n2
        expectedVariablesCount = n1*n2 + m1*m2
        #print(f"Expected number of variables: {expectedVariablesCount}")
        #print(f"Expected number of clauses: < {expectedClauseCount}")
        satInstance = SatInstance(expectedVariablesCount, expectedClauseCount)

        currentStep = 1
        stepCounter = f"{{step}}/{len(self.steps)}"

        # (1) Make sure that we have a proper image for each fluent of P2
        if 'FluentsImages' in self.steps:
            for i in range(n2):
                print(f"Step {stepCounter.format(step=currentStep)}: {progressBar(i/n2, 24)}", sep='', end='\r', flush=True)
                clause = [fToFId(i, j) for j in range(n1)]
                satInstance.addClause(clause)
                # Now with the unicity of the image (not the injectivity)
                for j in range(n1):
                    for k in range(n1):
                        if k != j:
                            clause = [-1*fToFId(i, j), -1*fToFId(i, k)]
                            satInstance.addClause(clause)

            print(f"{f'Step {stepCounter.format(step=currentStep)}: Done':<45}")
            currentStep += 1

        # (2) Image of operators, same as above
        if 'OperatorsImages' in self.steps:
            for i in range(m2):
                print(f"Step {stepCounter.format(step=currentStep)}: {progressBar(i/m2, 24)}", sep='', end='\r', flush=True)
                clause = [oToOId(i, j) for j in range(m1)]
                satInstance.addClause(clause)

                for j in range(m1):
                    for k in range(m1):
                        if k != j:
                            clause = [-1*oToOId(i, j), -1*oToOId(i, k)]
                            satInstance.addClause(clause)

            print(f"{f'Step {stepCounter.format(step=currentStep)}: Done':<45}")
            currentStep += 1

        # (3) Enforcing the morphism property
        if 'MorphismProperty' in self.steps:
            for i in range(m2):
                print(f"Step {stepCounter.format(step=currentStep)}: {progressBar(i/m2, 24)}", sep='', end='\r', flush=True)
                for j in range(m1):
                    # If we map o'_j to o_i, then for each fluent in the pre (eff) of o'_j, there should be its image in
                    # the pre (eff) of o_i
                    operator1 = problem1.getOperatorById(j)
                    operator2 = problem2.getOperatorById(i)

                    required_mappings = [(operator2.pre_pos, operator1.pre_pos),
                                         (operator2.pre_neg, operator1.pre_neg),
                                         (operator2.eff_pos, operator1.eff_pos),
                                         (operator2.eff_neg, operator1.eff_neg)]

                    for op2_list, op1_list in required_mappings:
                        for k in op2_list:
                            clause = [-1*oToOId(i, j)]
                            clause.extend([fToFId(k, l) for l in op1_list])
                            satInstance.addClause(clause)

            print(f"{f'Step {stepCounter.format(step=currentStep)}: Done':<45}")
            currentStep += 1


        # Make sure there is no superfluous fluents in the images
        if 'BijectionProperty' in self.steps:
            for i in range(m2):
                print(f"Step {stepCounter.format(step=currentStep)}: {progressBar(i/m2, 24)}", sep='', end='\r', flush=True)
                for j in range(m1):
                    operator1 = problem1.getOperatorById(j)
                    operator2 = problem2.getOperatorById(i)

                    operator1_lists = [operator1.pre_pos, operator1.pre_neg,
                                      operator1.eff_pos, operator1.eff_neg]

                    for op1_list in operator1_lists:
                        for l in op1_list:
                            clause = [-1*oToOId(i, j)]
                            clause.extend([fToFId(k, l) for k in range(n2)])
                            satInstance.addClause(clause)
            print(f"{f'Step {stepCounter.format(step=currentStep)}: Done':<45}")
            currentStep += 1

        # Enforce the injectivity of the morphism between operators
        if 'OperatorsInjectivity' in self.steps:
            for i in range(m1):
                print(f"Step {stepCounter.format(step=currentStep)}: {progressBar(i/m1, 24)}", sep='', end='\r', flush=True)

                for j in range(m2):
                    for k in range(m2):
                        if k != j:
                            clause = [-1*oToOId(j, i), -1*oToOId(k, i)]
                            satInstance.addClause(clause)

            print(f"{f'Step {stepCounter.format(step=currentStep)}: Done':<45}")
            currentStep += 1

        # Initial and goal states
        compareLists = []
        if 'InitialStateConservation' in self.steps:
            compareListsAux = []
            for i in range(0, 2):
                compareListsAux.append((problem1.getInitialState()[i], problem2.getInitialState()[i]))
            compareLists.append(compareListsAux)

        if 'GoalStateConservation' in self.steps:
            compareListsAux = []
            for i in range(0, 2):
                compareListsAux.append((problem1.getGoalState()[i], problem2.getGoalState()[i]))
            compareLists.append(compareListsAux)

        for compareList in compareLists:
            progress = 0
            totalLength = sum([len(l1) + len(l2) for l1, l2 in compareList])
            for varList1, varList2 in compareList:
                varListLength1 = len(varList1)
                varListLength2 = len(varList2)

                for index in range(varListLength2):
                    i = varList2[index]
                    print(f"Step {stepCounter.format(step=currentStep)}: {progressBar(progress/totalLength, 24)}", sep='', end='\r', flush=True)
                    clause = [fToFId(i, j) for j in varList1]
                    satInstance.addClause(clause)
                    progress += 1

                for index in range(varListLength1):
                    i = varList1[index]
                    print(f"Step {stepCounter.format(step=currentStep)}: {progressBar(progress/totalLength, 24)}", sep='', end='\r', flush=True)
                    clause = [fToFId(i, j) for j in varList2]
                    satInstance.addClause(clause)
                    progress += 1

            print(f"{f'Step {stepCounter.format(step=currentStep)}: Done':<45}")
            currentStep += 1

        print(f"Number of variables: {satInstance.getVariablesCount()}")
        print(f"Number of clauses: {satInstance.getClausesCount()}")
        return satInstance

    def interpretAssignment(self, problem1, problem2, assignment, outFile=sys.stdout):
        """
        Interpret a model of the formula that is built in convertToSAT, and write it in a legible
        format.
        """
        filler = ''.join(['=']*30)

        outFile.write(filler)
        outFile.write("\nFLUENTS\n")
        outFile.write(filler)
        outFile.write("\n")

        n1, m1 = problem1.getFluentCount(), problem1.getOperatorCount()
        n2, m2 = problem2.getFluentCount(), problem2.getOperatorCount()

        # Functions that help with the conversion from the problem's data to variables of the SAT formula
        fToFId, fIdToF, oToOId, oIdToO = self.getObjectsToIdFunctions(problem1, problem2)

        for k in range(1, n1 * n2 + 1):
            if assignment[k]:
                i, j = fIdToF(k)
                if self.verboseActionNames:
                    outFile.write(f"{problem2.getPredicateByVarId(i)} => {problem1.getPredicateByVarId(j)}\n")
                else:
                    outFile.write(f"{i} => {j}\n")

        outFile.write("\n")
        outFile.write(filler)
        outFile.write("\nOPERATORS\n")
        outFile.write(filler)
        outFile.write("\n")

        for k in range(n1*n2 + 1, n1*n2 + m1*m2 + 1):
            if assignment[k]:
                i, j = oIdToO(k)
                if self.verboseActionNames:
                    outFile.write(f"{problem2.prettyPrintActionByOpId(i)} => {problem1.prettyPrintActionByOpId(j)}\n")
                else:
                    outFile.write(f"{problem2.getActionByOpId(i)} => {problem1.getActionByOpId(j)}\n")



    def getObjectsToIdFunctions(self, problem1, problem2):
        """
        Return bijections between variables of the form o_ij or f_ij, and the appropriate
        subsets of [1, n]. Useful for interfacing with SAT solvers
        """
        n1, m1 = problem1.getFluentCount(), problem1.getOperatorCount()
        n2, m2 = problem2.getFluentCount(), problem2.getOperatorCount()

        # Functions that help with the conversion from the problem's data to variables of the SAT formula
        # Fluents / FluentsId
        fToFId = lambda i, j: (i * n1 + j) + 1
        fIdToF = lambda k: ((k - 1) // n1, (k - 1) % n1)
        # Operators / OperatorsId
        oToOId = lambda i, j: (i * m1 + j) + (n1 * n2 + 1)
        oIdToO = lambda k: ((k - n1 * n2 - 1) // m1, (k - n1 * n2 - 1) % m1)

        return fToFId, fIdToF, oToOId, oIdToO
