class StripsProblem:
    def __init__(self, predicate_to_varId, varId_to_predicate, action_to_opId, opId_to_action, opId_to_operator):
        # All mentions to PDDL refer to grounded PDDL predicates and actions
        # Convention: predicate in PDDL, variable in STRIPS
        self.predicate_to_varId = predicate_to_varId
        self.varId_to_predicate = varId_to_predicate

        # Convention: action in PDDL, operator in STRIPS
        self.action_to_opId = action_to_opId
        self.opId_to_action = opId_to_action
        self.opId_to_operator = opId_to_operator

    def prettyPrintActionByOpId(self, opId):
        """
        Pretty print a grounded STRIPS action
        """
        # TODO: rework it all, redundancy with something that is already in Grounder.py
        operator = self.opId_to_operator[opId]

        action_name = operator.name
        pre_pos, pre_neg = operator.pre_pos, operator.pre_neg
        eff_pos, eff_neg = operator.eff_pos, operator.eff_neg

        flat_fluents = [' '.join(map(lambda x: self.varId_to_predicate[x], l)) for l in [pre_pos, pre_neg, eff_pos, eff_neg]]
        pre_eff = ' '.join([f"({fluents})" for fluents in flat_fluents])
        return f"<{action_name}: {pre_eff}>"

    def getFluentName(self, varId):
        return self.varId_to_predicate[varId]

    def getOperatorName(self, operatorId):
        return self.opId_to_action[operatorId]

    def getFluents(self):
        for fluent in self.opId_to_action.keys():
            yield fluent

    def getOperatorsHashed(self):
        for operator in self.varId_to_predicate.keys():
            yield operator

    def getOperators(self):
        for operator in self.opId_to_operator.values():
            yield operator

    def getFluentCount(self):
        return len(self.varId_to_predicate)

    def getOperatorCount(self):
        return len(self.opId_to_action)

    def getPredicateByVarId(self, varId):
        return self.varId_to_predicate[varId]

    def getActionByOpId(self, opId):
        return self.opId_to_action[opId]

    def getOperatorById(self, opId):
        return self.opId_to_operator[opId]
