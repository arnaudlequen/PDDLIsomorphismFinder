from DomainListener import *
from InstanceListener import *
from StripsConverter import *
from SatInstance import *
from Utils import progress_bar


class SubisoFinder:
    def __init__(self):
        self.verbose_action_names = True

        self.pruning_steps = [
            'OperatorProfiling',
        ]

        self.sat_steps = [
            'FluentsImages',
            'OperatorsImages',
            'MorphismProperty',
            'BijectionProperty',
            'OperatorsInjectivity',
            # 'InitialStateConservation',
            # 'GoalStateConservation',
        ]

    def convert_to_sat(self, problem1: StripsProblem, problem2: StripsProblem, file_path: str = None):
        """
        Consider the problem STRIPS-subproblem-isomorphism(problem1, problem2), where one tries to find a subproblem of
        problem1 that is isomorphic to problem2. This function gives a SAT encoding of it.

        Args:
            problem1: The problem from which to find a subproblem that is isomorphic to problem2. An instance of
                StripsProblem
            problem2: The smaller problem
            file_path: The path to the file to which the intermediate SAT formula should be saved
        """
        n1, m1 = problem1.get_fluent_count(), problem1.get_operator_count()
        n2, m2 = problem2.get_fluent_count(), problem2.get_operator_count()

        if n1 < n2 or m1 < m2:
            print("The target problem is too big, no subproblem exists")
            return None

        # Functions that help with the conversion from the problem's data to variables of the SAT formula
        f_to_fid, fid_to_f, o_to_oid, oid_to_o = self.get_objects_to_id_functions(problem1, problem2)

        # Definition of the formula
        expected_clause_count = n2 + n2 * (n1 ** 2) + m2 + m2 * (m1 ** 2) \
                                + 4 * m2 * m1 * n2 + m1 * (m2 ** 2) + 2 * n1 + 2 * n2
        expected_variables_count = n1 * n2 + m1 * m2
        print(f"Maximum number of variables: {expected_variables_count}")
        print(f"Maximum number of clauses: < {expected_clause_count}")
        print()

        sat_instance = SatInstance(expected_variables_count)
        if file_path is not None:
            sat_instance.open_output_file(file_path)

        partial_assignment: List[bool | None] = [None] * (expected_variables_count + 1)

        if len(self.pruning_steps) > 0:
            # First round of simplification using local consistency checks
            current_step = 1
            step_counter = f"{{step}}/{len(self.pruning_steps)}"

            print("Performing pruning steps ...")
            fluent_matrix = [[True] * n1 for _ in range(n2)]  # f_m[i][j]: can fluent f'_i be mapped to f_j?
            operator_matrix = [[True] * m1 for _ in range(m2)]

            simplified_fluent_count = 0
            simplified_operator_count = 0

            # (1.1) Operators local consistency
            if 'OperatorProfiling' in self.pruning_steps:
                for i in range(m2):
                    oi_profile = problem2.get_operator_profile(i)
                    print(f"Step {step_counter.format(step=current_step)}: {progress_bar(i / m2, 24)}",
                          sep='', end='\r', flush=True)
                    for j in range(m1):
                        if oi_profile != problem1.get_operator_profile(j):

                            operator_matrix[i][j] = False
                            simplified_operator_count += 1

                step_end_str = f"Step {step_counter.format(step=current_step)}: Done"
                print(f"{step_end_str:<45}")

            print(f"Pruning done. Associations removed:")
            print(f"Fluents: {simplified_fluent_count} ({simplified_fluent_count / (n1 * n2) * 100:0.2f}%)")
            print(f"Operators: {simplified_operator_count} ({simplified_operator_count/(m1 * m2) * 100:0.2f}%)")
            print()

            index = 1
            for i in range(n2):
                for j in range(n1):
                    partial_assignment[index] = False if not fluent_matrix[i][j] else None
                    index += 1

            for i in range(m2):
                for j in range(m1):
                    partial_assignment[index] = False if not operator_matrix[i][j] else None
                    index += 1

            sat_instance.set_partial_assignment(partial_assignment)

        print("Generating SAT instance")

        # SAT creation phase
        current_step = 1
        step_counter = f"{{step}}/{len(self.sat_steps)}"

        # (1) Make sure that we have a proper image for each fluent of P2
        if 'FluentsImages' in self.sat_steps:
            for i in range(n2):
                print(f"Step {step_counter.format(step=current_step)}: {progress_bar(i / n2, 24)}",
                      sep='', end='\r', flush=True)
                clause = [f_to_fid(i, j) for j in range(n1)]
                sat_instance.add_clause(clause)
                # Now with the unicity of the image (not the injectivity)
                for j in range(n1):
                    for k in range(j + 1, n1):
                        clause = [-1 * f_to_fid(i, j), -1 * f_to_fid(i, k)]
                        sat_instance.add_clause(clause)

            step_end_str = f"Step {step_counter.format(step=current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses)"
            print(f"{step_end_str:<45}")
            current_step += 1

        # (2) Image of operators, same as above
        if 'OperatorsImages' in self.sat_steps:
            for i in range(m2):
                print(f"Step {step_counter.format(step=current_step)}: {progress_bar(i / m2, 24)}",
                      sep='', end='\r', flush=True)
                clause = [o_to_oid(i, j) for j in range(m1)]
                sat_instance.add_clause(clause)

                for j in range(m1):
                    for k in range(j + 1, m1):
                        clause = [-1 * o_to_oid(i, j), -1 * o_to_oid(i, k)]
                        sat_instance.add_clause(clause)

            step_end_str = f"Step {step_counter.format(step=current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses)"
            print(f"{step_end_str:<45}")
            current_step += 1

        # (3) Enforcing the morphism property
        if 'MorphismProperty' in self.sat_steps:
            for i in range(m2):
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
                            sat_instance.add_clause(clause)

            step_end_str = f"Step {step_counter.format(step=current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses)"
            print(f"{step_end_str:<45}")
            current_step += 1

        # Make sure there is no superfluous fluents in the images
        if 'BijectionProperty' in self.sat_steps:
            for i in range(m2):
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
                            sat_instance.add_clause(clause)
            step_end_str = f"Step {step_counter.format(step=current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses)"
            print(f"{step_end_str:<45}")
            current_step += 1

        # Enforce the injectivity of the morphism between operators
        if 'OperatorsInjectivity' in self.sat_steps:
            for i in range(m1):
                print(f"Step {step_counter.format(step=current_step)}: {progress_bar(i / m1, 24)}",
                      sep='', end='\r', flush=True)

                for j in range(m2):
                    for k in range(j + 1, m2):
                        clause = [-1 * o_to_oid(j, i), -1 * o_to_oid(k, i)]
                        sat_instance.add_clause(clause)

            step_end_str = f"Step {step_counter.format(step=current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses)"
            print(f"{step_end_str:<45}")
            current_step += 1

        # Initial and goal states
        compare_lists = []
        if 'InitialStateConservation' in self.sat_steps:
            compare_lists_aux = []
            for i in range(0, 2):
                compare_lists_aux.append((problem1.get_initial_state()[i], problem2.get_initial_state()[i]))
            compare_lists.append(compare_lists_aux)

        if 'GoalStateConservation' in self.sat_steps:
            compare_lists_aux = []
            for i in range(0, 2):
                compare_lists_aux.append((problem1.get_goal_state()[i], problem2.get_goal_state()[i]))
            compare_lists.append(compare_lists_aux)

        for compare_list in compare_lists:
            progress = 0
            total_length = sum([len(l1) + len(l2) for l1, l2 in compare_list])
            for var_list1, var_list2 in compare_list:

                back_and_forth_lists = [(var_list1, var_list2),
                                        (var_list2, var_list1)]

                for var_a, var_b in back_and_forth_lists:
                    for i in var_b:
                        print(f"Step {step_counter.format(step=current_step)}: "
                              f"{progress_bar(progress / total_length, 24)}",
                              sep='', end='\r', flush=True)
                        clause = [f_to_fid(i, j) for j in var_a]
                        sat_instance.add_clause(clause)
                        progress += 1

            step_end_str = f"Step {step_counter.format(step=current_step)}: Done " \
                           f"({sat_instance.get_new_clauses_count()} clauses)"
            print(f"{step_end_str:<45}")
            current_step += 1

        print(''.join(['-'] * 30))
        print(f"Number of variables: {sat_instance.get_variables_count()}")
        print(f"Number of clauses: {sat_instance.get_clauses_count()}")

        sat_instance.close_output_file()

        return sat_instance

    def interpret_assignment(self, problem1, problem2, assignment, out_file=sys.stdout):
        """
        Interpret a model of the formula that is built in convertToSAT, and write it in a legible
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
                if self.verbose_action_names:
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
