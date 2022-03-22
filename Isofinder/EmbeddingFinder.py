import collections
from enum import Enum
from DomainListener import *
from InstanceListener import *
from StripsConverter import *
from SatInstance import *
from Utils import progress_bar
from DataStructures import FluentOccurrences
from typing import List, Tuple


class VarType(Enum):
    FLUENT = 0
    OPERATOR = 1
    FUSEFUL = 2
    OACTIVE = 3


class EmbeddingFinder:
    def __init__(self):
        self.verbose_action_names = True

        self.current_step = 0
        self.clean_trace = False
        self.durations = {}

        self.pruning_steps = [
            'CPFluentsSets',
            'CPOperatorProfiling',
            'CPConstraintPropagation',
        ]

        self.sat_steps = [
            'FluentsImages',
            'FluentsInjectivity',
            'OperatorsImages',
            'MorphismInclusion',
            'MorphismReverseInclusion',
            'InitialStateConservation',
            'GoalStateConservation',
            'UsefulFluentsDefinition',
            'ActiveOperatorDefinition',
        ]

    def convert_to_sat(self, problem1: StripsProblem, problem2: StripsProblem, cp: bool, file_path: str = None,
                       clean_trace: bool = False):
        """
        Consider the problem STRIPS-subproblem-isomorphism(problem1, problem2), where one tries to find a subproblem of
        problem1 that is isomorphic to problem2. This function gives a SAT encoding of it.

        Args:
            problem1: The problem in which to embed the other one
            problem2: The problem to embed
            cp: Enable the constraint propagation preprocessing
            file_path: The path to the file to which the intermediate SAT formula should be saved
            clean_trace: Do not use carriage returns to print animated progress bars
        """
        # Progress bar handling
        sat_instance = None
        self.current_step = 0
        self.clean_trace = clean_trace

        small_filler = ''.join(['-'] * 30)

        n1, m1 = problem1.get_fluent_count(), problem1.get_operator_count()
        n2, m2 = problem2.get_fluent_count(), problem2.get_operator_count()

        # Durations of the various steps
        self.durations = {}

        if n2 > n1:
            print("Impossible to find an embedding: P does not have enough fluents")
            print("Exiting...")
            return None

        # Functions that help with the conversion from the problem's data to variables of the SAT formula
        satid = SatIdConverter(problem1, problem2)

        # Definition of the formula
        # TODO: adjust the formula below
        expected_clauses_count = n2 + n2 * (n1 ** 2) + m2 + m2 * (m1 ** 2) \
                                 + 4 * m2 * m1 * n2 + m1 * (m2 ** 2) + 2 * n1 + 2 * n2
        expected_variables_count = n1 * (n2 + 1) + m1 * (m2 + 1) + 1
        print(f"Maximum number of variables: {expected_variables_count}")
        print(f"Maximum number of clauses: < {expected_clauses_count}")
        print()

        # Initialize the SAT instance, which writes the formula on disk as it is built
        sat_instance = SatInstance(expected_variables_count, expected_clauses_count)
        if file_path is not None:
            sat_instance.open_output_file(file_path)

        partial_assignment: List[bool | None] = [None] * (expected_variables_count + 1)

        #
        # Constraint propagation step
        #
        if len(self.pruning_steps) > 0 and cp:
            self.current_step = 1

            print("Performing pruning steps ...")
            print(small_filler)

            # Initialize domains according to what steps are performed next
            domains = {'fluents': [],
                       'operators': [],
                       'fuseful': [],
                       'oactive': []}

            # Remark: domains concern fluents from P' and operators from P
            if 'CPFluentsSets' in self.pruning_steps:
                domains['fluents'] = [set() for _ in range(n2)]
            else:
                domains['fluents'] = [set(range(n1)) for _ in range(n2)]

            domains['operators'] = [set(range(m2)) for _ in range(m1)]
            domains['fuseful'] = [{True, False} for _ in range(n1)]
            domains['oactive'] = [{True, False} for _ in range(m1)]

            simplified_fluent_count = 0
            simplified_operator_count = 0

            # (1.1) Fluents initial and goal sets
            if 'CPFluentsSets' in self.pruning_steps and 'InitialStateConservation' in self.sat_steps and \
                'GoalStateConservation' in self.sat_steps:
                step_start = perf_counter()

                neutral_fluents = set(range(n2))
                neutral_fluents_image = set(range(n1))

                for k in [0, 1]:
                    neutral_fluents_image.difference_update(set(problem2.get_initial_state()[k]))
                    neutral_fluents_image.difference_update(set(problem2.get_goal_state()[k]))

                # Number of fluents that are simplified in the domain of neutral fluents (i.e., fluents not in I or G)
                simplified_non_neutral_fluents = n2 - len(neutral_fluents_image)

                progress = 0
                step_length = len(problem1.get_initial_state()[0]) + len(problem1.get_initial_state()[1]) + \
                              len(problem2.get_goal_state()[0]) + len(problem2.get_goal_state()[0])
                for k in [0, 1]:
                    for i in problem2.get_initial_state()[k]:
                        self.update_progress_bar('pruning', progress / step_length)
                        domains['fluents'][i] = set(problem1.get_initial_state()[k])
                        if i in neutral_fluents:
                            neutral_fluents.remove(i)
                            simplified_fluent_count += 1
                        progress += 1

                    for i in problem2.get_goal_state()[k]:
                        self.update_progress_bar('pruning', progress / step_length)
                        # If the domain of fluent i is already initialized, then it means that it is also in I
                        if len(domains['fluents'][i]) != 0:
                            domains['fluents'][i].intersection_update(problem1.get_goal_state()[k])
                        else:
                            domains['fluents'][i] = set(problem1.get_goal_state()[k])
                        if i in neutral_fluents:
                            neutral_fluents.remove(i)
                            simplified_fluent_count += 1

                for i in neutral_fluents:
                    domains['fluents'][i] = neutral_fluents_image.copy()
                    simplified_fluent_count += simplified_non_neutral_fluents

                self.end_step('CPFluentsSets', step_start, sat_instance)

            # (1.2) Operators local consistency
            if 'CPOperatorProfiling' in self.pruning_steps:
                step_start = perf_counter()

                for i in range(m1):
                    oi_profile = problem1.get_operator_profile(i)
                    self.update_progress_bar('pruning', i / m1)

                    for j in range(m2):
                        if not (oi_profile.leq(problem2.get_operator_profile(j))):
                            domains['operators'][i].remove(j)
                            simplified_operator_count += 1

                self.end_step('CPOperatorProfiling', step_start, sat_instance)

            # (1.3) Constraint propagation
            if 'CPConstraintPropagation' in self.pruning_steps:
                step_start = perf_counter()
                # Build the fluent -> action association tables
                fluent1_associations = [FluentOccurrences() for _ in range(problem1.get_fluent_count())]
                fluent2_associations = [FluentOccurrences() for _ in range(problem2.get_fluent_count())]

                for problem, fluent_associations in [(problem1, fluent1_associations),
                                                     (problem2, fluent2_associations)]:
                    for selector in [lambda x: x.pre_pos, lambda x: x.pre_neg,
                                     lambda x: x.eff_pos, lambda x: x.eff_neg]:
                        for op_id, op in problem.enumerate_operators():
                            for fluent in selector(op):
                                selector(fluent_associations[fluent]).add(op_id)

                # Main algorithm inspired by AC3 for constraint propagation
                items_list: List[Tuple[int, VarType]] \
                    = [(f, VarType.FLUENT) for f in range(problem2.get_fluent_count())]
                items_list.extend([(o, VarType.OPERATOR) for o in range(problem1.get_operator_count())])
                items_list.extend([(f, VarType.FUSEFUL) for f in range(problem1.get_fluent_count())])
                items_list.extend([(o, VarType.OACTIVE) for o in range(problem1.get_operator_count())])
                total_items_number = len(items_list)

                update_queue = collections.deque(items_list)

                # For debugging purpose
                force_additional_pass = 0

                while update_queue:
                    var, var_type = update_queue.pop()
                    self.update_progress_bar('pruning', len(update_queue) / total_items_number)

                    # Can be removed: mostly for debugging purposes
                    if force_additional_pass > 0 and not update_queue:
                        items_list = [(f, VarType.FLUENT) for f in range(problem2.get_fluent_count())]
                        items_list.extend((o, VarType.OPERATOR) for o in range(problem1.get_operator_count()))
                        update_queue = collections.deque(items_list)
                        force_additional_pass -= 1

                    # In case a fluent is up next
                    if var_type == VarType.FLUENT:
                        rm_count = self.cp_revise_fluents(var, domains, fluent1_associations, fluent2_associations)
                        # TODO: adapt this to account for the asymetries of the associations (F' -> F but O -> O')
                        if rm_count > 0:
                            simplified_fluent_count += rm_count
                            # Re-revise the domains of the operators o1 that "use" the fluent for which some candidate
                            # o2 was possibly supported by f2 = var
                            operators_to_add = set()
                            for selector in [lambda x: x.pre_pos, lambda x: x.pre_neg,
                                             lambda x: x.eff_pos, lambda x: x.eff_neg]:
                                for op2_id in selector(fluent2_associations[var]):
                                    for op1_id in domains['operators'][op2_id]:
                                        operators_to_add.add(op1_id)

                            for op1_id in operators_to_add:
                                # TODO: find out why there is a typing issue here
                                update_queue.append((op1_id, VarType.OPERATOR))

                    # In case an operator is up next
                    if var_type == VarType.OPERATOR:
                        rm_count = self.cp_revise_operators(var, domains, problem1, problem2)
                        if rm_count > 0:
                            simplified_operator_count += rm_count
                            op2 = problem2.get_operator_by_id(var)
                            for selector in [lambda x: x.pre_pos, lambda x: x.pre_neg,
                                             lambda x: x.eff_pos, lambda x: x.eff_neg]:
                                for fluent2 in selector(op2):
                                    update_queue.append((fluent2, VarType.FLUENT))

                    # In case a variable of type fluent_useful is up next
                    if var_type == VarType.FUSEFUL:
                        rm_count = self.cp_revise_fuseful(var, domains, problem1, fluent1_associations)
                        if rm_count > 0:
                            simplified_fluent_count += rm_count
                            # Re-revise the domains of the operators potentially made active by the fluent
                            for selector in [lambda x: x.eff_pos, lambda x: x.eff_neg]:
                                for op1_id in selector(fluent1_associations[var]):
                                    update_queue.append((op1_id, VarType.OPERATOR))

                    if var_type == VarType.OACTIVE:
                        # The variable is not used yet
                        pass

                self.end_step('CPConstraintPropagation', step_start, sat_instance)

            # Propagating the results to the SATInstance
            print(f"Pruning done. Associations removed:")
            print(f"Fluents: {simplified_fluent_count} ({simplified_fluent_count / (n1 * n2) * 100:0.2f}%)")
            print(f"Operators: {simplified_operator_count} ({simplified_operator_count / (m1 * m2) * 100:0.2f}%)")
            print()

            for i in range(n2):
                for j in set(range(n1)) - domains['fluents'][i]:
                    partial_assignment[satid.conv('fmap')(i, j)] = False

            for i in range(m2):
                for j in set(range(m1)) - domains['operators'][i]:
                    partial_assignment[satid.conv('omap')(i, j)] = False

            sat_instance.set_partial_assignment(partial_assignment)

        print("Generating SAT instance")
        print(small_filler)

        # SAT creation phase
        self.current_step = 1

        # (1) Make sure that we have a proper image for each fluent of P2
        # TODO: Iterate on D(f') instead of F, for instance
        if 'FluentsImages' in self.sat_steps:
            step_start = perf_counter()

            for j in range(n2):
                self.update_progress_bar('sat', j / n2)
                clause = [satid.conv('fmap')(i, j) for i in range(n1)]
                added_successfully = sat_instance.add_clause(clause)
                if not added_successfully:
                    return None, set()

                for i1 in range(n1):
                    for i2 in range(i1 + 1, n1):
                        clause = [-1 * satid.conv('fmap')(i1, j), -1 * satid.conv('fmap')(i2, j)]
                        added_successfully = sat_instance.add_clause(clause)
                        if not added_successfully:
                            return None, set()

            self.end_step('FluentsImages', step_start, sat_instance)

        if 'FluentsInjectivity' in self.sat_steps:
            step_start = perf_counter()

            for i in range(n1):
                self.update_progress_bar('sat', i / n2)
                for j in range(n2):
                    for k in range(j + 1, n2):
                        clause = [-1 * satid.conv('fmap')(i, j), -1 * satid.conv('fmap')(i, k)]
                        added_successfully = sat_instance.add_clause(clause)
                        if not added_successfully:
                            return None, set()

            self.end_step('FluentsInjectivity', step_start, sat_instance)

        if 'OperatorsImages' in self.sat_steps:
            step_start = perf_counter()

            for i in range(m1):
                self.update_progress_bar('sat', i / m1)
                clause = [satid.conv('omap')(i, j) for j in range(m2)]
                clause.append(-1 * satid.conv('oact')(i))
                added_successfully = sat_instance.add_clause(clause)
                if not added_successfully:
                    return None, set()

                for j in range(m2):
                    for k in range(j + 1, m2):
                        clause = [-1 * satid.conv('omap')(i, j), -1 * satid.conv('omap')(i, k)]
                        added_successfully = sat_instance.add_clause(clause)
                        if not added_successfully:
                            return None, set()

            self.end_step('OperatorsImages', step_start, sat_instance)

        if 'MorphismInclusion' in self.sat_steps:
            step_start = perf_counter()

            for o in range(m1):
                self.update_progress_bar('sat', o / m1)
                for k in range(m2):
                    operator1 = problem1.get_operator_by_id(o)
                    operator2 = problem2.get_operator_by_id(k)

                    required_mappings = [(operator1.pre_pos, operator2.pre_pos),
                                         (operator1.pre_neg, operator2.pre_neg),
                                         (operator1.eff_pos, operator2.eff_pos),
                                         (operator1.eff_neg, operator2.eff_neg)]

                    for f1_list, f2_list in required_mappings:
                        for j in f2_list:
                            clause = [-1 * satid.conv('oact')(o), -1 * satid.conv('omap')(o, k)]
                            clause.extend([satid.conv('fmap')(i, j) for i in f1_list])

                            added_successfully = sat_instance.add_clause(clause)
                            if not added_successfully:
                                return None, set()

            self.end_step('MorphismInclusion', step_start, sat_instance)

        if 'MorphismReverseInclusion' in self.sat_steps:
            step_start = perf_counter()

            for o in range(m1):
                self.update_progress_bar('sat', o / m1)
                for k in range(m2):
                    operator1 = problem1.get_operator_by_id(o)
                    operator2 = problem2.get_operator_by_id(k)

                    required_mappings = [(operator1.eff_pos, operator2.eff_pos),
                                         (operator1.eff_neg, operator2.eff_neg)]

                    for f1_list, f2_list in required_mappings:
                        for i in f1_list:
                            clause = [-1 * satid.conv('fuse')(i), -1 * satid.conv('omap')(o, k)]
                            clause.extend([satid.conv('fmap')(i, j) for j in f2_list])

                            added_successfully = sat_instance.add_clause(clause)
                            if not added_successfully:
                                return None, set()

            self.end_step('MorphismReverseInclusion', step_start, sat_instance)

        if 'InitialStateConservation' in self.sat_steps:
            step_start = perf_counter()

            # We need to compare positive fluents together, and negative fluents together
            compare_lists = []
            for i in range(0, 2):
                compare_lists.append((problem1.get_initial_state()[i], problem2.get_initial_state()[i]))
            total_length = len(problem2.get_initial_state()[0]) + len(problem2.get_initial_state()[1])

            progress = 0
            for f1_init, f2_init in compare_lists:
                for i in f1_init:
                    progress += 1
                    self.update_progress_bar('sat', progress / total_length)
                    clause = [-1 * satid.conv('fuse')(i)]
                    clause.extend([satid.conv('fmap')(i, j) for j in f2_init])

                    added_successfully = sat_instance.add_clause(clause)
                    if not added_successfully:
                        return None, set()

            self.end_step('InitialStateConservation', step_start, sat_instance)

        if 'GoalStateConservation' in self.sat_steps:
            step_start = perf_counter()

            compare_lists = []
            for i in range(0, 2):
                compare_lists.append((problem1.get_goal_state()[i], problem2.get_goal_state()[i]))
            total_length = len(problem2.get_goal_state()[0]) + len(problem2.get_goal_state()[1])

            progress = 0
            for f1_goal, f2_goal in compare_lists:
                for j in f2_goal:
                    progress += 1
                    self.update_progress_bar('sat', progress / total_length)
                    clause = [satid.conv('fmap')(i, j) for i in f1_goal]

                    added_successfully = sat_instance.add_clause(clause)
                    if not added_successfully:
                        return None, set()

            self.end_step('GoalStateConservation', step_start, sat_instance)

        if 'UsefulFluentsDefinition' in self.sat_steps:
            step_start = perf_counter()

            for i in range(n1):
                clause = [satid.conv('fmap')(i, j) for j in range(n2)]
                clause.append(-1 * satid.conv('fuse')(i))

                added_successfully = sat_instance.add_clause(clause)
                if not added_successfully:
                    return None, set()

                for j in range(n2):
                    clause = [satid.conv('fuse')(i), -1 * satid.conv('fmap')(i, j)]
                    added_successfully = sat_instance.add_clause(clause)
                    if not added_successfully:
                        return None, set()

            self.end_step('UsefulFluentsDefinition', step_start, sat_instance)

        if 'ActiveOperatorDefinition' in self.sat_steps:
            step_start = perf_counter()

            for i in range(n1):
                for o in range(m1):
                    if i in problem1.get_operator_by_id(i).eff_pos or i in problem1.get_operator_by_id(i).eff_neg:
                        clause = [-1 * satid.conv('fuse')(i), satid.conv('oact')(o)]

                        added_successfully = sat_instance.add_clause(clause)
                        if not added_successfully:
                            return None, set()

            self.end_step('ActiveOperatorDefinition', step_start, sat_instance)

        print(''.join(['-'] * 30))
        print(f"Number of variables: {sat_instance.get_variables_count()} "
              f"({sat_instance.get_simplified_variables_count()} simplified)")
        print(f"Number of clauses: {sat_instance.get_clauses_count()} "
              f"({sat_instance.get_simplified_clauses_count()} simplified)")

        # The SAT formula is written on disk: write the meta-data and close the file
        sat_instance.close_output_file()

        return sat_instance, self.durations

    @staticmethod
    def cp_revise_operators(op2_id, domains, problem1: StripsProblem, problem2: StripsProblem) -> int:
        """
        Revise the possibilities of affectations of operator `operator` of problem 2 to the operators of problem 1.
        Modifies in place the various matrices

        Return
            The number of associations that the algorithm removed
        """
        removed_candidates = 0

        op2 = problem2.get_operator_by_id(op2_id)

        for op1_id in domains['operators'][op2_id].copy():
            op1 = problem1.get_operator_by_id(op1_id)
            keep_operator = True

            attributes_lists = [(op1.pre_pos, op2.pre_pos),
                                (op1.pre_neg, op2.pre_neg),
                                (op1.eff_pos, op2.eff_pos),
                                (op1.eff_neg, op2.eff_neg)]

            # Check if there exists a fluent in op2_lst that can't be mapped to a fluent of op1_lst
            for op1_lst, op2_lst in attributes_lists:
                for fluent1_id in op1_lst:
                    if domains['fuseful'][fluent1_id] != {True}:
                        continue

                    # The fluent is useful and is related to o1, so it has to be matched
                    fluent_matched = False

                    for fluent2_id in op2_lst:
                        if fluent1_id in domains['fluents'][fluent2_id]:
                            fluent_matched = True
                            break

                    if not fluent_matched:
                        keep_operator = False

            if not keep_operator:
                # if op1_id in domains['operators'][op2_id]:  # There should be no need for this line
                domains['operators'][op2_id].remove(op1_id)
                removed_candidates += 1

        return removed_candidates

    @staticmethod
    def cp_revise_fluents(fluent2_id, domains, fluents1_associations: List[FluentOccurrences],
                          fluents2_associations: List[FluentOccurrences]) -> int:
        """
        Revise the possibilities of affectations of the fluent of id fluent2_id of problem 2, to fluents of problem1.
        Modifies in place the various matrices

        Return
            The number of associations that the algorithm removed
        """
        removed_candidates = 0

        for fluent1_id in domains['fluents'][fluent2_id].copy():
            keep_fluent = True

            # Check that f can be useful
            if True not in domains['fuseful'][fluent1_id]:
                keep_fluent = False

            # Check that for each o1 in which f1 appears in the effect, there is another o2 (in D(o1) in which f2
            # appears with the same sign
            for selector_eff in [lambda x: x.eff_pos, lambda x: x.eff_neg]:
                for operator1_id in selector_eff(fluents1_associations[fluent1_id]):
                    # Check if there is an o2 in the domain of o1, that also has f2 in its effect, with the correct sign
                    if not (domains['operators'][operator1_id] & selector_eff(fluents2_associations[fluent2_id])):
                        keep_fluent = False
                        break

                if not keep_fluent:
                    break

            if not keep_fluent:
                domains['fluents'][fluent2_id].remove(fluent1_id)
                removed_candidates += 1

        return removed_candidates

    @staticmethod
    def cp_revise_fuseful(fluent1_id, domains, problem2: StripsProblem,
                          fluents1_associations: List[FluentOccurrences]) -> int:
        """
        Revise the usefulness of fluent fluent1_id

        Return
            The number of possible values that the algorithm removed
        """
        candidate_domain = {True, False}

        # Check whether True belongs to the domain or not
        # First condition: some other fluent must have it in its domain
        live_candidate = False
        for fluent2_domain in domains['fluents']:
            if fluent1_id in fluent2_domain:
                live_candidate = True
                break

        if not live_candidate:
            candidate_domain.remove(True)

        # Second condition: if f1 activates the action o1, then it has to be matched by some other fluent f2 in some
        # image o2 of o1
        # For each o1 that has f1 in its effect:
        for selector_eff in [lambda x: x.eff_pos, lambda x: x.eff_neg]:
            if True not in candidate_domain:
                break

            for operator1_id in selector_eff(fluents1_associations[fluent1_id]):
                if True not in candidate_domain:
                    break

                # Find an operator o2 (candidate v(o1) = o2) that has a suitable candidate f2 that can make f1 useful
                matched_operator = False
                for operator2_id in domains['operators'][operator1_id]:
                    op2 = problem2.get_operator_by_id(operator2_id)
                    for fluent2_id in selector_eff(op2):
                        if fluent1_id in domains['fluents'][fluent2_id]:
                            matched_operator = True
                            break
                    if matched_operator:
                        break

                if not matched_operator:
                    candidate_domain.remove(True)

        # Check whether False belongs to the domain or not
        for fluent2_domain in domains['fluents']:
            if fluent2_domain == {fluent1_id}:
                candidate_domain.remove(False)
                break

        # Number of elements that have been added or removed
        changed = len(candidate_domain.symmetric_difference(domains['fuseful'][fluent1_id]))
        domains['fuseful'][fluent1_id] = candidate_domain

        return changed

    def interpret_assignment(self, problem1: StripsProblem, problem2: StripsProblem, assignment,
                             actions_name_only=False, out_file=sys.stdout):
        """
        Interpret a model of the formula that is built in convert_to_sat, and write it in a legible
        format.
        """
        filler = ''.join(['='] * 30)

        out_file.write(filler)
        out_file.write("\nFLUENTS\n")
        out_file.write(filler)
        out_file.write("\n")

        n1, m1 = problem1.get_fluent_count(), problem1.get_operator_count()
        n2, m2 = problem2.get_fluent_count(), problem2.get_operator_count()

        # Functions that help with the conversion from the problem's data to variables of the SAT formula
        satid = SatIdConverter(problem1, problem2)

        for k in range(1, n1 * n2 + 1):
            if assignment[k]:
                i, j = satid.conv('fmap', -1)(k)
                if self.verbose_action_names:
                    out_file.write(f"{problem2.get_predicate_by_var_id(i)} => {problem1.get_predicate_by_var_id(j)}\n")
                else:
                    out_file.write(f"{i} => {j}\n")

        out_file.write("\n")
        out_file.write(filler)
        out_file.write("\nOPERATORS\n")
        out_file.write(filler)
        out_file.write("\n")

        for k in range(n1 * n2 + 1, n1 * n2 + m1 * m2 + 1):
            if assignment[k]:
                i, j = satid.conv('omap', -1)(k)
                if actions_name_only:
                    out_file.write(f"{problem2.get_action_by_op_id(i)} => "
                                   f"{problem1.get_action_by_op_id(j)}\n")
                elif self.verbose_action_names:
                    out_file.write(f"{problem2.pretty_print_action_by_op_id(i)} => "
                                   f"{problem1.pretty_print_action_by_op_id(j)}\n")
                else:
                    out_file.write(f"{problem2.get_action_by_op_id(i)} => "
                                   f"{problem1.get_action_by_op_id(j)}\n")

    def update_progress_bar(self, phase, percentage):
        step_count = 0
        match phase:
            case 'pruning':
                step_count = len(self.pruning_steps)
            case 'sat':
                step_count = len(self.sat_steps)
        step_counter = f"{{step}}/{step_count}"
        if self.clean_trace:
            return
        print(f"Step {step_counter.format(step=self.current_step)}: {progress_bar(percentage, 24)}",
              sep='', end='\r', flush=True)

    def end_step(self, step, step_start, sat_instance):
        logging_names = {'CPFluentsSets': 'sat_fluents_sets',
                         'CPOperatorProfiling': 'sat_operator_profiling',
                         'CPConstraintPropagation': 'sat_constraint_propagation_time',
                         'FluentsImages': 'sat_translation_fluents_images',
                         'FluentsInjectivity': 'sat_translation_fluents_injectivity',
                         'OperatorsImages': 'sat_translation_operators_images',
                         'MorphismInclusion': 'sat_translation_morphism_inclusion',
                         'MorphismReverseInclusion': 'sat_translation_morphism_reverse_inclusion',
                         'InitialStateConservation': 'sat_translation_init_state_conservation',
                         'GoalStateConservation': 'sat_translation_goal_conservation',
                         'UsefulFluentsDefinition': 'sat_translation_useful_fluents_def',
                         'ActiveOperatorDefinition': 'sat_translation_active_operators_def',
                         }

        if step.startswith('CP'):
            step_count = len(self.pruning_steps)
        else:
            step_count = len(self.sat_steps)

        step_counter = f"{{step}}/{step_count}"

        if step.startswith('CP'):
            step_end_str = f"Step {step_counter.format(step=self.current_step)}: Done "
        else:
            step_end_str = f"Step {step_counter.format(step=self.current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses, " \
                           f"{sat_instance.get_new_simplified_clauses_count()} simplified)"
        self.durations[logging_names[step]] = perf_counter() - step_start  # Todo: convert step to something else (ex. FluentsImages -> sat_translation_fluents_images)
        print(f"{step_end_str:<45}")
        self.current_step += 1


class SatIdConverter:
    def __init__(self, problem1: StripsProblem, problem2: StripsProblem):
        # n1 >= n2 but m1 and m2 are not comparable in general
        n1, m1 = problem1.get_fluent_count(), problem1.get_operator_count()
        n2, m2 = problem2.get_fluent_count(), problem2.get_operator_count()

        # Dictionary that contains functions to convert fluents and operators to variables id for the SAT formula
        # Convention: first argument is either fluent/operator, then the type of the variable in the SAT formula,
        # and then 0 for the conversion STRIPS problem -> SAT variable id, or 1 (or -1) for the converse
        self.converters = {}

        # Fill the dictionary above with the functions that we need
        # Convention: first argument for P, second argument for P'
        # Associations between fluents of P and P'
        offset0 = 1

        fmap = [lambda i, j: (j * n1 + i) + offset0,
                lambda k: ((k - offset0) % n1, (k - offset0) // n1)]
        self.converters['fmap'] = fmap
        offset1 = n1 * n2 + offset0

        # Operators / OperatorsId
        if m1 >= m2:
            omap = [lambda i, j: (j * m1 + i) + offset1,
                    lambda k: ((k - offset2) % m1, (k - offset1) // m1)]
        else:
            omap = [lambda i, j: (i * m2 + j) + offset1,
                    lambda k: ((k - offset1) // m2, (k - offset1) % m2)]
        self.converters['omap'] = omap
        offset2 = m1 * m2 + offset1

        # Fluents / UsefulFluentId
        fuse = [lambda i: i + offset2,
                lambda k: k - offset2]
        self.converters['fuse'] = fuse
        offset3 = n1 + offset2

        # Operators / ActiveOperatorId
        oact = [lambda i: i + offset3,
                lambda k: k - offset3]
        self.converters['oact'] = oact

    def conversion_function(self, sat_variable, direction=1):
        """
        Return the conversion function from the object of type problem_item to a variable_id of type sat_var, or the
        converse if direction is non-positive
        """
        assert sat_variable in ['fmap', 'fuse', 'omap', 'oact']

        if direction == 1:
            return self.converters[sat_variable][0]
        elif direction == -1:
            return self.converters[sat_variable][1]

        return None

    def conv(self, sat_variable, direction=1):
        return self.conversion_function(sat_variable, direction)





