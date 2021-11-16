class StripsProblem:
    def __init__(self, predicate_to_var_id, var_id_to_predicate, action_to_op_id, op_id_to_action, op_id_to_operator,
                 initial_state_variables_pos, initial_state_variables_neg,
                 goal_state_variables_pos, goal_state_variables_neg):
        # All mentions to PDDL refer to grounded PDDL predicates and actions
        # Convention: predicate in PDDL, variable in STRIPS
        self.predicate_to_varId = predicate_to_var_id
        self.varId_to_predicate = var_id_to_predicate

        # Convention: action in PDDL, operator in STRIPS
        self.action_to_opId = action_to_op_id
        self.opId_to_action = op_id_to_action
        self.opId_to_operator = op_id_to_operator

        self.init_pos = initial_state_variables_pos
        self.init_neg = initial_state_variables_neg
        self.goal_pos = goal_state_variables_pos
        self.goal_neg = goal_state_variables_neg

    def pretty_print_action_by_op_id(self, op_id):
        """
        Pretty print a grounded STRIPS action
        """
        # TODO: rework it all, redundancy with something that is already in Grounder.py
        operator = self.opId_to_operator[op_id]

        action_name = operator.name
        pre_pos, pre_neg = operator.pre_pos, operator.pre_neg
        eff_pos, eff_neg = operator.eff_pos, operator.eff_neg

        flat_fluents = [' '.join(map(lambda x: self.varId_to_predicate[x], l)) for l in [pre_pos, pre_neg, eff_pos, eff_neg]]
        pre_eff = ' '.join([f"({fluents})" for fluents in flat_fluents])
        return f"<{action_name}: {pre_eff}>"

    def get_initial_state(self):
        return self.init_pos, self.init_neg

    def get_goal_state(self):
        return self.goal_pos, self.goal_neg

    def get_fluent_name(self, var_id):
        return self.varId_to_predicate[var_id]

    def get_operator_name(self, op_id):
        return self.opId_to_action[op_id]

    def get_fluents(self):
        for fluent in self.opId_to_action.keys():
            yield fluent

    def get_operators_hashed(self):
        for operator in self.varId_to_predicate.keys():
            yield operator

    def get_operators(self):
        for operator in self.opId_to_operator.values():
            yield operator

    def get_fluent_count(self):
        return len(self.varId_to_predicate)

    def get_operator_count(self):
        return len(self.opId_to_action)

    def get_predicate_by_var_id(self, var_id):
        return self.varId_to_predicate[var_id]

    def get_var_id_by_predicate(self, predicate):
        return self.predicate_to_varId[predicate]

    def get_action_by_op_id(self, op_id):
        return self.opId_to_action[op_id]

    def get_operator_by_id(self, op_id):
        return self.opId_to_operator[op_id]
