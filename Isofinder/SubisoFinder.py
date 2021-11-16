from DomainListener import *
from InstanceListener import *
from StripsConverter import *
from SatInstance import *
from Utils import progressBar


class SubisoFinder:
    def __init__(self):
        self.verboseActionNames = True

        self.steps = [
            'FluentsImages',
            'OperatorsImages',
            'MorphismProperty',
            'BijectionProperty',
            'OperatorsInjectivity',
            # 'InitialStateConservation',
            # 'GoalStateConservation',
        ]

    def convert_to_sat(self, problem1, problem2):
        """
        Consider the problem STRIPS-subproblem-isomorphism(problem1, problem2), where one tries to find a subproblem of
        problem1 that is isomorphic to problem2. This function gives a SAT encoding of it.

        Args:
            problem1: The problem from which to find a subproblem that is isomorphic to problem2. An instance of
                StripsProblem
            problem2: The smaller problem
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
        # print(f"Expected number of variables: {expected_variables_count}")
        # print(f"Expected number of clauses: < {expected_clause_count}")
        sat_instance = SatInstance(expected_variables_count, expected_clause_count)

        current_step = 1
        step_counter = f"{{step}}/{len(self.steps)}"

        # (1) Make sure that we have a proper image for each fluent of P2
        if 'FluentsImages' in self.steps:
            for i in range(n2):
                print(f"Step {step_counter.format(step=current_step)}: {progressBar(i / n2, 24)}",
                      sep='', end='\r', flush=True)
                clause = [f_to_fid(i, j) for j in range(n1)]
                sat_instance.add_clause(clause)
                # Now with the unicity of the image (not the injectivity)
                for j in range(n1):
                    for k in range(n1):
                        if k != j:
                            clause = [-1 * f_to_fid(i, j), -1 * f_to_fid(i, k)]
                            sat_instance.add_clause(clause)

            print(f"{f'Step {step_counter.format(step=current_step)}: Done':<45}")
            current_step += 1

        # (2) Image of operators, same as above
        if 'OperatorsImages' in self.steps:
            for i in range(m2):
                print(f"Step {step_counter.format(step=current_step)}: {progressBar(i / m2, 24)}",
                      sep='', end='\r', flush=True)
                clause = [o_to_oid(i, j) for j in range(m1)]
                sat_instance.add_clause(clause)

                for j in range(m1):
                    for k in range(m1):
                        if k != j:
                            clause = [-1 * o_to_oid(i, j), -1 * o_to_oid(i, k)]
                            sat_instance.add_clause(clause)

            print(f"{f'Step {step_counter.format(step=current_step)}: Done':<45}")
            current_step += 1

        # (3) Enforcing the morphism property
        if 'MorphismProperty' in self.steps:
            for i in range(m2):
                print(f"Step {step_counter.format(step=current_step)}: {progressBar(i / m2, 24)}",
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

            print(f"{f'Step {step_counter.format(step=current_step)}: Done':<45}")
            current_step += 1

        # Make sure there is no superfluous fluents in the images
        if 'BijectionProperty' in self.steps:
            for i in range(m2):
                print(f"Step {step_counter.format(step=current_step)}: {progressBar(i / m2, 24)}",
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
            print(f"{f'Step {step_counter.format(step=current_step)}: Done':<45}")
            current_step += 1

        # Enforce the injectivity of the morphism between operators
        if 'OperatorsInjectivity' in self.steps:
            for i in range(m1):
                print(f"Step {step_counter.format(step=current_step)}: {progressBar(i / m1, 24)}",
                      sep='', end='\r', flush=True)

                for j in range(m2):
                    for k in range(m2):
                        if k != j:
                            clause = [-1 * o_to_oid(j, i), -1 * o_to_oid(k, i)]
                            sat_instance.add_clause(clause)

            print(f"{f'Step {step_counter.format(step=current_step)}: Done':<45}")
            current_step += 1

        # Initial and goal states
        compare_lists = []
        if 'InitialStateConservation' in self.steps:
            compare_lists_aux = []
            for i in range(0, 2):
                compare_lists_aux.append((problem1.get_initial_state()[i], problem2.get_initial_state()[i]))
            compare_lists.append(compare_lists_aux)

        if 'GoalStateConservation' in self.steps:
            compare_lists_aux = []
            for i in range(0, 2):
                compare_lists_aux.append((problem1.get_goal_state()[i], problem2.get_goal_state()[i]))
            compare_lists.append(compare_lists_aux)

        for compareList in compare_lists:
            progress = 0
            total_length = sum([len(l1) + len(l2) for l1, l2 in compareList])
            for var_list1, var_list2 in compareList:

                back_and_forth_lists = [(var_list1, var_list2),
                                        (var_list2, var_list1)]

                for var_a, var_b in back_and_forth_lists:
                    for i in var_b:
                        print(f"Step {step_counter.format(step=current_step)}: "
                              f"{progressBar(progress / total_length, 24)}",
                              sep='', end='\r', flush=True)
                        clause = [f_to_fid(i, j) for j in var_a]
                        sat_instance.add_clause(clause)
                        progress += 1

            print(f"{f'Step {step_counter.format(step=current_step)}: Done':<45}")
            current_step += 1

        print(f"Number of variables: {sat_instance.get_variables_count()}")
        print(f"Number of clauses: {sat_instance.get_clauses_count()}")
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
                if self.verboseActionNames:
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
                if self.verboseActionNames:
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
