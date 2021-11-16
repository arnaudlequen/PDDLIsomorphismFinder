from ASTypes import *
from DomainListener import *
from InstanceListener import *
from StripsProblem import StripsProblem
from time import perf_counter
import itertools as it


class Grounder:
    def __init__(self):
        self.pddlDomain = None
        self.pddlInstance = None

        # Convention: predicate in PDDL, variable in STRIPS
        self.predicate_to_var_id = {}
        self.var_id_to_predicate = {}

        # Convention: action in PDDL, operator in STRIPS
        self.action_to_op_id = {}
        self.op_id_to_action = {}
        self.op_id_to_operator = {}

        # Convention: fluents encoded in varId
        self.init_pos = []
        self.init_neg = []
        self.goal_pos = []
        self.goal_neg = []

    def ground_instance(self, pddl_domain, pddl_instance):
        print(f"Grounding instance {pddl_instance.name} of domain {pddl_domain.name}")

        self.pddlDomain = pddl_domain
        self.pddlInstance = pddl_instance

        # Reset
        self.predicate_to_var_id = {}
        self.var_id_to_predicate = {}

        self.action_to_op_id = {}
        self.op_id_to_action = {}
        self.op_id_to_operator = {}

        global_start_time = perf_counter()
        print("Grounding predicates...")
        start_time = perf_counter()
        self.ground_predicates()
        stop_time = perf_counter()
        print(f"DONE. Found {self.get_variables_count()} fluents in {stop_time - start_time:.4f}s")

        print("Grounding actions...")
        start_time = perf_counter()
        self.ground_actions()
        stop_time = perf_counter()
        print(f"DONE. Found {self.get_operators_count()} operators in {stop_time - start_time:.4f}s")

        print("Encoding initial and goal states...")
        start_time = perf_counter()
        self.build_initial_and_goal_states()
        stop_time = perf_counter()
        print(f"DONE. Conversion done in {stop_time - start_time:.4f}s")

        print(f"=> Grounding completed in {perf_counter() - start_time:.4f}s")

        return StripsProblem(self.predicate_to_var_id, self.var_id_to_predicate,
                             self.action_to_op_id, self.op_id_to_action,
                             self.op_id_to_operator,
                             self.init_pos, self.init_neg,
                             self.goal_pos, self.goal_neg)

    def ground_predicates(self):
        """
        Ground the predicates and create the variables
        """
        for predicate in self.pddlDomain.predicates:
            # One can check if the value that is returned is True or False, to determine whether the grounding was
            # successful or not
            self.ground_predicates_aux(predicate.name, predicate.arguments_type_list, [])

    def ground_predicates_aux(self, predicate_name, predicate_types_list, current_arguments_list):
        """
        Auxiliary function that explores a branch of the grounding tree

        Args:
            predicate_name:         The name of the current predicate
            predicate_types_list:   The types of the arguments of the predicates that are left to ground
            current_arguments_list: The name of the current arguments that have already been grounded

        Returns:
            True if and only if a correct grounding has been false
            False otherwise
        """
        objects_dictionary = self.pddlInstance.objects

        # Base case
        if predicate_types_list == []:
            self.register_new_variable(predicate_name, current_arguments_list)
            return True

        # Recursion: take each object of the correct type and recursively call the function
        curr_type = predicate_types_list[0]
        if curr_type in objects_dictionary:
            next_predicate_types_list = predicate_types_list[1:]
            for obj in objects_dictionary[curr_type]:
                next_arguments_list = current_arguments_list[:]
                next_arguments_list.append(obj)
                grounding_outcome = self.ground_predicates_aux(predicate_name, next_predicate_types_list,
                                                               next_arguments_list)
                if not grounding_outcome:
                    # If there is an issue during the grounding of the predicate, then it means that a type has no
                    # existing object, and the predicate will never be able to be grounded
                    return False
            return True
        return False

    def register_new_variable(self, predicate_name, arguments_list):
        """
        Add a variable to the (grounded) STRIPS problem
        """
        hashed_predicate = self.hash_ground_predicate(predicate_name, arguments_list)
        predicate_id = len(self.predicate_to_var_id)
        self.predicate_to_var_id[hashed_predicate] = predicate_id
        self.var_id_to_predicate[predicate_id] = hashed_predicate

    def ground_actions(self):
        """
        Ground the actions
        """
        actions = self.pddlDomain.actions
        objects_dictionary = self.pddlInstance.objects

        for action in actions:
            # Create pairs (type, parameter_name) for each parameter in the parameters dictionary
            parameters_type_list = list(it.chain.from_iterable(
                [list(zip([param_type] * len(args), args)) for param_type, args in action.parameters.items()]))
            self.find_param_assignment(action, parameters_type_list, {})

    def find_param_assignment(self, action, parameters, assignment):
        """
        Recursively build an assignment for the parameters, and register the grounded action (= operator) when all
        parameters of the action have been assigned

        Args:
            action: The action to ground
            parameters: A list of pairs (type, parameter_name) that constitute the parameters of the action
            assignment: The current assignment of the parameters, a dictionary param_name -> object
        """
        # Base case
        if parameters == []:
            self.register_new_action(action, assignment)
            return True

        # Recursion: try to ground the remaining parameters
        objects_dictionary = self.pddlInstance.objects

        current_param = parameters[0]
        param_type, param_name = current_param[0], current_param[1]
        if param_type not in objects_dictionary:
            return False

        for obj in objects_dictionary[param_type]:
            new_assignment = assignment.copy()
            new_assignment[param_name] = obj
            self.find_param_assignment(action, parameters[1:], new_assignment)

        return True

    def register_new_action(self, action, assignment):
        # Even though we have the assignment, we still need to build the action

        # Preconditions and effects of the action
        pre_pos = []
        pre_neg = []
        eff_pos = []
        eff_neg = []

        for relation, predicate_list in [('pre', action.precondition), ('eff', action.effects)]:
            for literal in predicate_list:
                # sign = 1 if literal.sign == '+' else 0
                # rel = 1 if relation == 'eff' else 0
                action_predicate = literal.predicate

                grounded_args = []
                for param_type, arg in zip(action_predicate.arguments_type_list, action_predicate.arguments_name_list):
                    # One can also check the type, even though we do not do it here
                    grounded_args.append(assignment[arg])

                # Add the variable id to the relevant precondition list
                hashed_ground_predicate = self.hash_ground_predicate(action_predicate.name, grounded_args)
                variable_id = self.predicate_to_var_id[hashed_ground_predicate]

                # [pre_neg, pre_pos, eff_neg, eff_pos][sign + 2*rel].append(variable_id)
                if relation == 'pre':
                    if literal.sign == '+':
                        pre_pos.append(variable_id)
                    elif literal.sign == '-':
                        pre_neg.append(variable_id)
                elif relation == 'eff':
                    if literal.sign == '+':
                        eff_pos.append(variable_id)
                    elif literal.sign == '-':
                        eff_neg.append(variable_id)

        operator_id = len(self.action_to_op_id)
        hashed_ground_action = self.hash_ground_action(action.name, pre_pos, pre_neg, eff_pos, eff_neg)
        operator = Operator(action.name, pre_pos, pre_neg, eff_pos, eff_neg)

        self.action_to_op_id[hashed_ground_action] = operator_id
        self.op_id_to_action[operator_id] = hashed_ground_action
        self.op_id_to_operator[operator_id] = operator

    def build_initial_and_goal_states(self):
        """
        Convert the grounded predicates found in the initial and goal states of an instance file to the variable id
        that is assigned to them in the grounding previously done
        """
        convert_lists = [(self.pddlInstance.init, self.init_pos, self.init_neg),
                         (self.pddlInstance.goal, self.goal_pos, self.goal_neg)]

        for literals_list, varIds_pos, varIds_neg in convert_lists:
            for hashed_literal in literals_list:
                if hashed_literal.predicate in self.predicate_to_var_id:
                    predicate_id = self.predicate_to_var_id[hashed_literal.predicate]
                    if hashed_literal.sign == '+':
                        varIds_pos.append(predicate_id)
                    else:
                        varIds_neg.append(predicate_id)

    def hash_ground_action(self, action_name, pre_pos, pre_neg, eff_pos, eff_neg):
        flat_fluents = [' '.join(map(str, l)) for l in [pre_pos, pre_neg, eff_pos, eff_neg]]
        pre_eff = ' '.join([f"({fluents})" for fluents in flat_fluents])
        return f"<{action_name}: {pre_eff}>"

    def hash_ground_action_pp(self, action_name, pre_pos, pre_neg, eff_pos, eff_neg):
        """
        Hash a ground action (= operator) and return a pretty-printable version
        """
        flat_fluents = [' '.join(map(lambda x: self.var_id_to_predicate[x], l)) for l in
                        [pre_pos, pre_neg, eff_pos, eff_neg]]
        pre_eff = ' '.join([f"({fluents})" for fluents in flat_fluents])
        return f"<{action_name}: {pre_eff}>"

    def unhash_ground_action(self, hashed_ground_action):
        action_name, relations = hashed_ground_action[1:-1].split(": ")
        pre_pos, pre_neg, eff_pos, eff_neg = list(
            map(lambda x: list(map(int, x.rstrip()[:-1].split())), relations.split('(')[1:]))

        return action_name, pre_pos, pre_neg, eff_pos, eff_neg

    def unhash_ground_action_to_operator(self, hashed_ground_action):
        return Operator(*self.unhash_ground_action(hashed_ground_action))

    def hash_ground_predicate(self, predicate_name, arguments_list):
        return f"({predicate_name} {' '.join(arguments_list)})"

    def unhash_ground_predicate(self, hashed_ground_predicate):
        """
        Unhash the grounded predicates that have been hashed in order to be stored in the hashmaps
        of the grounder

        Return:
            A pair that consists of the name of the predicate and of a list of the names of the objects
            that make up the predicate
        """
        elements = hashed_ground_predicate[1:-1].split(' ')
        return elements[0], elements[1:]

    def get_variables_count(self):
        return len(self.var_id_to_predicate)

    def get_operators_count(self):
        return len(self.op_id_to_action)
