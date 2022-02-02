import collections

from DomainListener import *
from InstanceListener import *
from StripsConverter import *
from SatInstance import *
from Utils import progress_bar
from DataStructures import FluentOccurrences


class SubisoFinder:
    def __init__(self):
        self.verbose_action_names = True

        self.pruning_steps = [
            'OperatorProfiling',
            'ConstraintPropagation',
        ]

        self.sat_steps = [
            'FluentsImages',
            'OperatorsImages',
            'MorphismProperty',
            'BijectionProperty',
            'FluentsInjectivity',
            'OperatorsInjectivity',
            # 'InitialStateConservation',
            # 'GoalStateConservation',
        ]

    def convert_to_sat(self, problem1: StripsProblem, problem2: StripsProblem, nocp: bool, file_path: str = None,
                       clean_trace: bool = False):
        """
        Consider the problem STRIPS-subproblem-isomorphism(problem1, problem2), where one tries to find a subproblem of
        problem1 that is isomorphic to problem2. This function gives a SAT encoding of it.

        Args:
            problem1: The problem from which to find a subproblem that is isomorphic to problem2. An instance of
                StripsProblem
            problem2: The smaller problem
            file_path: The path to the file to which the intermediate SAT formula should be saved
        """
        small_filler = ''.join(['-'] * 30)

        n1, m1 = problem1.get_fluent_count(), problem1.get_operator_count()
        n2, m2 = problem2.get_fluent_count(), problem2.get_operator_count()

        # Durations of the various steps
        durations = {}

        if n1 < n2 or m1 < m2:
            print("The target problem is too big: switching problems...")
            problem3 = problem1
            problem1 = problem2
            problem2 = problem3
            n1, m1 = problem1.get_fluent_count(), problem1.get_operator_count()
            n2, m2 = problem2.get_fluent_count(), problem2.get_operator_count()

        # Functions that help with the conversion from the problem's data to variables of the SAT formula
        f_to_fid, fid_to_f, o_to_oid, oid_to_o = self.get_objects_to_id_functions(problem1, problem2)

        # Definition of the formula
        expected_clauses_count = n2 + n2 * (n1 ** 2) + m2 + m2 * (m1 ** 2) \
                                + 4 * m2 * m1 * n2 + m1 * (m2 ** 2) + 2 * n1 + 2 * n2
        expected_variables_count = n1 * n2 + m1 * m2
        print(f"Maximum number of variables: {expected_variables_count}")
        print(f"Maximum number of clauses: < {expected_clauses_count}")
        print()

        sat_instance = SatInstance(expected_variables_count, expected_clauses_count)
        if file_path is not None:
            sat_instance.open_output_file(file_path)

        partial_assignment: List[bool | None] = [None] * (expected_variables_count + 1)

        # Pruning impossible mappings
        if len(self.pruning_steps) > 0 and not nocp:
            current_step = 1
            step_counter = f"{{step}}/{len(self.pruning_steps)}"

            print("Performing pruning steps ...")
            print(small_filler)
            fluents_domain = [set(range(n1)) for _ in range(n2)]  # f_m[i][j]: can fluent f'_i be mapped to f_j?
            operators_domain = [set(range(m1)) for _ in range(m2)]

            simplified_fluent_count = 0
            simplified_operator_count = 0

            # (1.1) Operators local consistency
            if 'OperatorProfiling' in self.pruning_steps:
                step_start = perf_counter()
                for i in range(m2):
                    oi_profile = problem2.get_operator_profile(i)
                    if not clean_trace:
                        print(f"Step {step_counter.format(step=current_step)}: {progress_bar(i / m2, 24)}",
                              sep='', end='\r', flush=True)
                    for j in range(m1):
                        if oi_profile != problem1.get_operator_profile(j):

                            operators_domain[i].remove(j)
                            simplified_operator_count += 1

                step_end_str = f"Step {step_counter.format(step=current_step)}: Done"
                print(f"{step_end_str:<45}")
                durations['sat_operator_profiling_time'] = perf_counter() - step_start
                current_step += 1

            # (1.2) Constraint propagation
            if 'ConstraintPropagation' in self.pruning_steps:
                step_start = perf_counter()
                # Build the fluent -> action association table
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
                items_list = [(f, 0) for f in range(problem2.get_fluent_count())]
                items_list.extend((o, 1) for o in range(problem2.get_operator_count()))
                total_items_number = len(items_list)

                update_queue = collections.deque(items_list)

                # For debugging purpose
                force_additional_pass = 0

                while update_queue:
                    var, var_type = update_queue.pop()
                    if not clean_trace:
                        print(f"Step {step_counter.format(step=current_step)}: "
                              f"{progress_bar(len(update_queue) / total_items_number, 24)}",
                              sep='', end='\r', flush=True)

                    # Can be removed: mostly for debugging purposes
                    if force_additional_pass > 0 and not update_queue:
                        items_list = [(f, 0) for f in range(problem2.get_fluent_count())]
                        items_list.extend((o, 1) for o in range(problem2.get_operator_count()))
                        update_queue = collections.deque(items_list)
                        force_additional_pass -= 1

                    # In case a fluent is up next
                    if var_type == 0:
                        rm_count = self.cp_revise_fluents(var, operators_domain, fluents_domain,
                                                          fluent1_associations, fluent2_associations)
                        if rm_count > 0:
                            simplified_fluent_count += rm_count
                            # Re-revise the domains of the operators that "use" the fluent
                            for selector in [lambda x: x.pre_pos, lambda x: x.pre_neg,
                                             lambda x: x.eff_pos, lambda x: x.eff_neg]:
                                for op2_id in selector(fluent2_associations[var]):
                                    # TODO: check that we are adding correctly the associations that we need
                                    update_queue.append((op2_id, 1))

                    if var_type == 1:
                        rm_count = self.cp_revise_operators(var, operators_domain, fluents_domain, problem1, problem2)
                        if rm_count > 0:
                            simplified_operator_count += rm_count
                            op2 = problem2.get_operator_by_id(var)
                            for selector in [lambda x: x.pre_pos, lambda x: x.pre_neg,
                                             lambda x: x.eff_pos, lambda x: x.eff_neg]:
                                for fluent2 in selector(op2):
                                    update_queue.append((fluent2, 0))

                step_end_str = f"Step {step_counter.format(step=current_step)}: Done"
                print(f"{step_end_str:<45}")
                durations['sat_constraint_propagation_time'] = perf_counter() - step_start
                current_step += 1

            # Propagating the results to the SATInstance
            print(f"Pruning done. Associations removed:")
            print(f"Fluents: {simplified_fluent_count} ({simplified_fluent_count / (n1 * n2) * 100:0.2f}%)")
            print(f"Operators: {simplified_operator_count} ({simplified_operator_count/(m1 * m2) * 100:0.2f}%)")
            print()

            for i in range(n2):
                for j in set(range(n1)) - fluents_domain[i]:
                    partial_assignment[f_to_fid(i, j)] = False

            for i in range(m2):
                for j in set(range(m1)) - operators_domain[i]:
                    partial_assignment[o_to_oid(i, j)] = False

            sat_instance.set_partial_assignment(partial_assignment)

        print("Generating SAT instance")
        print(small_filler)

        # SAT creation phase
        current_step = 1
        step_counter = f"{{step}}/{len(self.sat_steps)}"

        # (1) Make sure that we have a proper image for each fluent of P2
        if 'FluentsImages' in self.sat_steps:
            step_start = perf_counter()
            for i in range(n2):
                if not clean_trace:
                    print(f"Step {step_counter.format(step=current_step)}: {progress_bar(i / n2, 24)}",
                          sep='', end='\r', flush=True)

                clause = [f_to_fid(i, j) for j in range(n1)]
                added_successfully = sat_instance.add_clause(clause)
                if not added_successfully:
                    return None, set()

                # Now with the unicity of the image (not the injectivity)
                for j in range(n1):
                    for k in range(j + 1, n1):
                        clause = [-1 * f_to_fid(i, j), -1 * f_to_fid(i, k)]
                        added_successfully = sat_instance.add_clause(clause)
                        if not added_successfully:
                            return None, set()

            step_end_str = f"Step {step_counter.format(step=current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses, " \
                           f"{sat_instance.get_new_simplified_clauses_count()} simplified)"
            durations['sat_fluents_images_time'] = perf_counter() - step_start
            print(f"{step_end_str:<45}")
            current_step += 1

        # (2) Image of operators, same as above
        if 'OperatorsImages' in self.sat_steps:
            step_start = perf_counter()
            for i in range(m2):
                if not clean_trace:
                    print(f"Step {step_counter.format(step=current_step)}: {progress_bar(i / m2, 24)}",
                          sep='', end='\r', flush=True)
                clause = [o_to_oid(i, j) for j in range(m1)]
                added_successfully = sat_instance.add_clause(clause)
                if not added_successfully:
                    return None, set()

                for j in range(m1):
                    for k in range(j + 1, m1):
                        clause = [-1 * o_to_oid(i, j), -1 * o_to_oid(i, k)]
                        added_successfully = sat_instance.add_clause(clause)
                        if not added_successfully:
                            return None, set()

            step_end_str = f"Step {step_counter.format(step=current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses, " \
                           f"{sat_instance.get_new_simplified_clauses_count()} simplified)"
            durations['sat_operators_images_time'] = perf_counter() - step_start
            print(f"{step_end_str:<45}")
            current_step += 1

        # (3) Enforcing the morphism property
        if 'MorphismProperty' in self.sat_steps:
            step_start = perf_counter()
            for i in range(m2):
                if not clean_trace:
                    print(f"Step {step_counter.format(step=current_step)}: {progress_bar(i / m2, 24)}",
                          sep='', end='\r', flush=True)
                for j in range(m1):
                    # If we map o'_j to o_i, then for each fluent in the pre (eff) of o'_j, there should be its image in
                    # the pre (eff) of o_i
                    operator1 = problem1.get_operator_by_id(j)
                    operator2 = problem2.get_operator_by_id(i)

                    required_mappings = [(operator2.pre_pos, operator1.pre_pos),
                                         (operator2.pre_neg, operator1.pre_neg),
                                         (operator2.eff_pos, operator1.eff_pos),
                                         (operator2.eff_neg, operator1.eff_neg)]

                    for op2_list, op1_list in required_mappings:
                        for k in op2_list:
                            clause = [-1 * o_to_oid(i, j)]
                            clause.extend([f_to_fid(k, l) for l in op1_list])
                            added_successfully = sat_instance.add_clause(clause)
                            if not added_successfully:
                                return None, set()

            step_end_str = f"Step {step_counter.format(step=current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses, " \
                           f"{sat_instance.get_new_simplified_clauses_count()} simplified)"
            durations['sat_morphism_property_time'] = perf_counter() - step_start
            print(f"{step_end_str:<45}")
            current_step += 1

        # Make sure there is no superfluous fluents in the images
        if 'BijectionProperty' in self.sat_steps:
            step_start = perf_counter()
            for i in range(m2):
                if not clean_trace:
                    print(f"Step {step_counter.format(step=current_step)}: {progress_bar(i / m2, 24)}",
                          sep='', end='\r', flush=True)
                for j in range(m1):
                    operator1 = problem1.get_operator_by_id(j)

                    operator1_lists = [operator1.pre_pos, operator1.pre_neg,
                                       operator1.eff_pos, operator1.eff_neg]

                    for op1_list in operator1_lists:
                        for l in op1_list:
                            clause = [-1 * o_to_oid(i, j)]
                            clause.extend([f_to_fid(k, l) for k in range(n2)])
                            added_successfully = sat_instance.add_clause(clause)
                            if not added_successfully:
                                return None, set()
            step_end_str = f"Step {step_counter.format(step=current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses, " \
                           f"{sat_instance.get_new_simplified_clauses_count()} simplified)"
            durations['sat_bijection_property_time'] = perf_counter() - step_start
            print(f"{step_end_str:<45}")
            current_step += 1

        # Enforce the injectivity of the morphism between fluents
        if 'FluentsInjectivity' in self.sat_steps:
            step_start = perf_counter()
            for i in range(n1):
                if not clean_trace:
                    print(f"Step {step_counter.format(step=current_step)}: {progress_bar(i / n1, 24)}",
                          sep='', end='\r', flush=True)

                for j in range(n2):
                    for k in range(j + 1, n2):
                        clause = [-1 * f_to_fid(j, i), -1 * f_to_fid(k, i)]
                        added_successfully = sat_instance.add_clause(clause)
                        if not added_successfully:
                            return None, set()

            step_end_str = f"Step {step_counter.format(step=current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses, " \
                           f"{sat_instance.get_new_simplified_clauses_count()} simplified)"
            durations['sat_fluents_injectivity_time'] = perf_counter() - step_start
            print(f"{step_end_str:<45}")
            current_step += 1

        # Enforce the injectivity of the morphism between operators
        if 'OperatorsInjectivity' in self.sat_steps:
            step_start = perf_counter()
            for i in range(m1):
                if not clean_trace:
                    print(f"Step {step_counter.format(step=current_step)}: {progress_bar(i / m1, 24)}",
                          sep='', end='\r', flush=True)

                for j in range(m2):
                    for k in range(j + 1, m2):
                        clause = [-1 * o_to_oid(j, i), -1 * o_to_oid(k, i)]
                        added_successfully = sat_instance.add_clause(clause)
                        if not added_successfully:
                            return None, set()

            step_end_str = f"Step {step_counter.format(step=current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses, " \
                           f"{sat_instance.get_new_simplified_clauses_count()} simplified)"
            durations['sat_operators_injectivity_time'] = perf_counter() - step_start
            print(f"{step_end_str:<45}")
            current_step += 1

        # Initial and goal states
        compare_lists = []
        if 'InitialStateConservation' in self.sat_steps:
            step_start = perf_counter()
            compare_lists_aux = []
            for i in range(0, 2):
                compare_lists_aux.append((problem1.get_initial_state()[i], problem2.get_initial_state()[i]))
            compare_lists.append(compare_lists_aux)
            durations['sat_initial_state_time'] = perf_counter() - step_start

        if 'GoalStateConservation' in self.sat_steps:
            step_start = perf_counter()
            compare_lists_aux = []
            for i in range(0, 2):
                compare_lists_aux.append((problem1.get_goal_state()[i], problem2.get_goal_state()[i]))
            compare_lists.append(compare_lists_aux)
            durations['sat_goal_state_time'] = perf_counter() - step_start

        for compare_list in compare_lists:
            progress = 0
            total_length = sum([len(l1) + len(l2) for l1, l2 in compare_list])
            for var_list1, var_list2 in compare_list:

                back_and_forth_lists = [(var_list1, var_list2),
                                        (var_list2, var_list1)]

                for var_a, var_b in back_and_forth_lists:
                    for i in var_b:
                        if not clean_trace:
                            print(f"Step {step_counter.format(step=current_step)}: "
                                  f"{progress_bar(progress / total_length, 24)}",
                                  sep='', end='\r', flush=True)
                        clause = [f_to_fid(i, j) for j in var_a]
                        added_successfully = sat_instance.add_clause(clause)
                        if not added_successfully:
                            return None, set()
                        progress += 1

            step_end_str = f"Step {step_counter.format(step=current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses, " \
                           f"{sat_instance.get_new_simplified_clauses_count()} simplified)"
            print(f"{step_end_str:<45}")
            current_step += 1

        print(''.join(['-'] * 30))
        print(f"Number of variables: {sat_instance.get_variables_count()} "
              f"({sat_instance.get_simplified_variables_count()} simplified)")
        print(f"Number of clauses: {sat_instance.get_clauses_count()} "
              f"({sat_instance.get_simplified_clauses_count()} simplified)")

        sat_instance.close_output_file()

        return sat_instance, durations

    def cp_revise_operators(self, op2_id, operators_domain, fluents_domain,
                            problem1: StripsProblem, problem2: StripsProblem) -> int:
        """
        Revise the possibilities of affectations of operator `operator` of problem 2 to the operators of problem 1.
        Modifies in place the various matrices

        Update
            operators_domain

        Return
            Whether the possible candidates to the image of the operator have changed or not
        """
        removed_candidates = 0

        op2 = problem2.get_operator_by_id(op2_id)

        for op1_id in operators_domain[op2_id].copy():
            op1 = problem1.get_operator_by_id(op1_id)
            attributes_lists = [(op1.pre_pos, op2.pre_pos),
                                (op1.pre_neg, op2.pre_neg),
                                (op1.eff_pos, op2.eff_pos),
                                (op1.eff_neg, op2.eff_neg)]

            # Check if there exists a fluent in op2_lst that can't be mapped to a fluent of op1_lst
            for op1_lst, op2_lst in attributes_lists:
                for fluent2 in op2_lst:
                    removable = True

                    for fluent1 in op1_lst:
                        if fluent1 in fluents_domain[fluent2]:
                            removable = False
                            break

                    if removable:
                        if op1_id in operators_domain[op2_id]:
                            operators_domain[op2_id].remove(op1_id)
                            removed_candidates += 1

        return removed_candidates

    def cp_revise_fluents(self, fluent2_id, operators_domain, fluents_domain,
                          fluents1_associations: List[FluentOccurrences],
                          fluents2_associations: List[FluentOccurrences]) -> int:
        """
        Revise the possibilities of affectations of the fluent of id fluent2_id of problem 2, to fluents of problem1.
        Modifies in place the various matrices

        Update
            fluents_matrix

        Return
            Whether the possible candidates to the image of the fluent have changed or not
        """
        removed_candidates = 0

        for fluent1_id in fluents_domain[fluent2_id].copy():
            keep_fluent = True

            for selector in [lambda x: x.pre_pos, lambda x: x.pre_neg,
                             lambda x: x.eff_pos, lambda x: x.eff_neg]:
                # For each operator where f2 appears in a list, there should be an equivalent operator where
                # f1 appears in the equivalent list (eg. positive precondition, etc.), if we want to map f2 to f1
                for operator2_id in selector(fluents2_associations[fluent2_id]):
                    # Seek an operator in problem1 that operator2 could be mapped to
                    removable = True
                    for operator1_id in selector(fluents1_associations[fluent1_id]):
                        if operator1_id in operators_domain[operator2_id]:
                            removable = False
                            break
                    if removable:
                        keep_fluent = False
                        break

                if not keep_fluent:
                    fluents_domain[fluent2_id].remove(fluent1_id)
                    removed_candidates += 1
                    break

        return removed_candidates

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
        f_to_fid, fid_to_f, o_to_oid, oid_to_o = self.get_objects_to_id_functions(problem1, problem2)

        for k in range(1, n1 * n2 + 1):
            if assignment[k]:
                i, j = fid_to_f(k)
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
                i, j = oid_to_o(k)
                if actions_name_only:
                    out_file.write(f"{problem2.get_action_by_op_id(i)} => "
                                   f"{problem1.get_action_by_op_id(j)}\n")
                elif self.verbose_action_names:
                    out_file.write(f"{problem2.pretty_print_action_by_op_id(i)} => "
                                   f"{problem1.pretty_print_action_by_op_id(j)}\n")
                else:
                    out_file.write(f"{problem2.get_action_by_op_id(i)} => "
                                   f"{problem1.get_action_by_op_id(j)}\n")

    @staticmethod
    def get_objects_to_id_functions(problem1, problem2):
        """
        Return bijections between variables of the form o_ij or f_ij, and the appropriate
        subsets of [1, n]. Useful for interfacing with SAT solvers
        """
        n1, m1 = problem1.get_fluent_count(), problem1.get_operator_count()
        n2, m2 = problem2.get_fluent_count(), problem2.get_operator_count()

        # Functions that help with the conversion from the problem's data to variables of the SAT formula
        # Fluents / FluentsId
        f_to_fid = lambda i, j: (i * n1 + j) + 1
        fid_to_f = lambda k: ((k - 1) // n1, (k - 1) % n1)
        # Operators / OperatorsId
        o_to_oid = lambda i, j: (i * m1 + j) + (n1 * n2 + 1)
        oid_to_o = lambda k: ((k - n1 * n2 - 1) // m1, (k - n1 * n2 - 1) % m1)

        return f_to_fid, fid_to_f, o_to_oid, oid_to_o
