from ASTypes import *
from DomainListener import *
from InstanceListener import *
from StripsProblem import StripsProblem
from time import time
import itertools as it

class Grounder():
    def __init__(self):
        self.pddlDomain = None
        self.pddlInstance = None

        # Convention: predicate in PDDL, variable in STRIPS
        self.predicate_to_varId = {}
        self.varId_to_predicate = {}

        # Convention: action in PDDL, operator in STRIPS
        self.action_to_opId = {}
        self.opId_to_action = {}
        self.opId_to_operator = {}

    def groundInstance(self, pddlDomain, pddlInstance):
        print(f"Grounding instance {pddlInstance.name} of domain {pddlDomain.name}")

        self.pddlDomain = pddlDomain
        self.pddlInstance = pddlInstance

        # Reset
        self.predicate_to_varId = {}
        self.varId_to_predicate = {}

        self.action_to_opId = {}
        self.opId_to_action = {}
        self.opId_to_operator = {}

        global_start_time = time()
        print("Grounding predicates...")
        start_time = time()
        self.ground_predicates()
        stop_time = time()
        print(f"DONE. Found {self.getVariablesCount()} fluents in {stop_time - start_time:.4f}s")

        print("Grounding actions...")
        start_time = time()
        self.ground_actions()
        stop_time = time()
        print(f"DONE. Found {self.getOperatorsCount()} operators in {stop_time - start_time:.4f}s")

        print(f"=> Gounding completed in {time()-start_time:.4f}s")

        return StripsProblem(self.predicate_to_varId, self.varId_to_predicate, \
                             self.action_to_opId, self.opId_to_action, \
                             self.opId_to_operator)

    def ground_predicates(self):
        """
        Ground the predicates and create the variables
        """
        objects_dictionary = self.pddlInstance.objects

        for predicate in self.pddlDomain.predicates:
            # One can check if the value that is returned is True or False, to determine whether the grounding was
            # successful or not
            self.ground_predicates_aux(predicate.name, predicate.arguments_type_list, [])

    def ground_predicates_aux(self, predicate_name, predicate_types_list, current_arguments_list):
        """
        Auxilliary function that explores a branch of the grounding tree

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
            for object in objects_dictionary[curr_type]:
                next_arguments_list = current_arguments_list[:]
                next_arguments_list.append(object)
                grounding_outcome = self.ground_predicates_aux(predicate_name, next_predicate_types_list, next_arguments_list)
                if grounding_outcome == False:
                    # If there is an issue during the grounding of the predicate, then it means that a type has no existing
                    # object, and the predicate will never be able to be grounded
                    return False
            return True
        return False

    def register_new_variable(self, predicate_name, arguments_list):
        """
        Add a variable to the (grounded) STRIPS problem
        """
        hashed_predicate = self.hash_ground_predicate(predicate_name, arguments_list)
        predicate_id = len(self.predicate_to_varId)
        self.predicate_to_varId[hashed_predicate] = predicate_id
        self.varId_to_predicate[predicate_id] = hashed_predicate

    def ground_actions(self):
        """
        Ground the actions
        """
        actions = self.pddlDomain.actions
        objects_dictionary = self.pddlInstance.objects

        for action in actions:
            # Create pairs (type, parameter_name) for each parameter in the parameters dictionary
            parameters_type_list = list(it.chain.from_iterable([list(zip([type]*len(args), args)) for type, args in action.parameters.items()]))
            self.find_param_assignment(action, parameters_type_list, {})
            #param_dic = {}
            #for type, param_list in action.parameters.items():
            #    for param in param_list:

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
        if not param_type in objects_dictionary:
            return False

        for object in objects_dictionary[param_type]:
            new_assignment = assignment.copy()
            new_assignment[param_name] = object
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
                #sign = 1 if literal.sign == '+' else 0
                #rel = 1 if relation == 'eff' else 0
                action_predicate = literal.predicate

                grounded_args = []
                for type, arg in zip(action_predicate.arguments_type_list, action_predicate.arguments_name_list):
                    # One can also check the type, even though we do not do it here
                    grounded_args.append(assignment[arg])

                # Add the variable id to the relevant precondition list
                hashed_ground_predicate = self.hash_ground_predicate(action_predicate.name, grounded_args)
                variable_id = self.predicate_to_varId[hashed_ground_predicate]

                #[pre_neg, pre_pos, eff_neg, eff_pos][sign + 2*rel].append(variable_id)
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

        operator_id = len(self.action_to_opId)
        hashed_ground_action = self.hash_ground_action(action.name, pre_pos, pre_neg, eff_pos, eff_neg)
        operator = Operator(action.name, pre_pos, pre_neg, eff_pos, eff_neg)

        self.action_to_opId[hashed_ground_action] = operator_id
        self.opId_to_action[operator_id] = hashed_ground_action
        self.opId_to_operator[operator_id] = operator

    def hash_ground_action(self, action_name, pre_pos, pre_neg, eff_pos, eff_neg):
        flat_fluents = [' '.join(map(str, l)) for l in [pre_pos, pre_neg, eff_pos, eff_neg]]
        pre_eff = ' '.join([f"({fluents})" for fluents in flat_fluents])
        return f"<{action_name}: {pre_eff}>"

    def hash_ground_action_pp(self, action_name, pre_pos, pre_neg, eff_pos, eff_neg):
        """
        Hash a ground action (= operator) and return a pretty-printable version
        """
        flat_fluents = [' '.join(map(lambda x: self.varId_to_predicate[x], l)) for l in [pre_pos, pre_neg, eff_pos, eff_neg]]
        pre_eff = ' '.join([f"({fluents})" for fluents in flat_fluents])
        return f"<{action_name}: {pre_eff}>"

    def unhash_ground_action(self, hashed_ground_action):
        action_name, relations = hashed_ground_action[1:-1].split(": ")
        pre_pos, pre_neg, eff_pos, eff_neg = list(map(lambda x: list(map(int, x.rstrip()[:-1].split())), relations.split('(')[1:]))

        return action_name, pre_pos, pre_neg, eff_pos, eff_neg

    def unhash_ground_action_to_operator(self, hashed_ground_action):
        return Operator(*unhash_ground_action(self, hashed_ground_action))

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

    def getVariablesCount(self):
        return len(self.varId_to_predicate)

    def getOperatorsCount(self):
        return len(self.opId_to_action)
