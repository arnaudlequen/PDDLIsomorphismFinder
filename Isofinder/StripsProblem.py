import attr
from ASTypes import *
from DataStructures import OperatorProfile
from typing import List, Dict


@attr.s
class StripsProblem:
    predicate_to_varId: dict = attr.ib()
    varId_to_predicate: dict = attr.ib()

    # All mentions to PDDL refer to grounded PDDL predicates and actions
    # Convention: action in PDDL, operator in STRIPS
    action_to_opId: dict = attr.ib()
    opId_to_action: dict = attr.ib()
    opId_to_operator: Dict[int, Operator] = attr.ib()

    init_pos: dict = attr.ib()
    init_neg: dict = attr.ib()
    goal_pos: dict = attr.ib()
    goal_neg: dict = attr.ib()

    # Statistics
    max_pre_arity: int = attr.ib(init=False, default=0)
    max_eff_arity: int = attr.ib(init=False, default=0)

    # Constraint iteration
    operators_profiles: List[OperatorProfile] = attr.ib(init=False)

    def __attrs_post_init__(self):
        m = len(self.opId_to_action)

        # There must be a way to initialize this otherwise
        self.operators_profiles = [OperatorProfile()] * m

        for i in range(m):
            op = self.opId_to_operator[i]

            prep_to_effn = len(set(op.pre_pos).intersection(set(op.eff_neg)))
            pren_to_effp = len(set(op.pre_neg).intersection(set(op.eff_pos)))

            op_profile = OperatorProfile(len(op.pre_pos), len(op.pre_neg),
                                         len(op.eff_pos), len(op.eff_neg),
                                         prep_to_effn, pren_to_effp)

            self.operators_profiles[i] = op_profile

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

    def enumerate_operators(self):
        return enumerate(self.opId_to_operator.values())

    def get_operator_profile(self, op_id: int):
        return self.operators_profiles[op_id]

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
