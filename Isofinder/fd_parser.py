from time import perf_counter
import parser.fdtranslate.pddl_parser as pddl_parser
from parser.fdtranslate.instantiate import explore

from strips_problem import StripsProblem, Operator

filler = '=' * 30
small_filler = '-' * 30


def fd_parser(args):
    print("Parsing problem 1")
    print(small_filler)
    problem1 = fd_parser_aux(args.domain1Path, args.instance1Path)
    print(small_filler)
    print("Done")
    print()

    print("Parsing problem 2")
    print(small_filler)
    problem2 = fd_parser_aux(args.domain2Path, args.instance2Path)
    print(small_filler)
    print("Done")
    print()

    return problem1, problem2


def fd_parser_aux(domain_path, instance_path):
    """
    Extract STRIPS instances out of PDDL files and return STRIPSProblem instances
    """
    # Extract problems from file
    global_start = perf_counter()
    print("Calling FastDownward's parser...")
    print(small_filler)

    task = pddl_parser.open(domain_path, instance_path)
    relaxed_reachable, atoms, actions, _, _ = explore(task)

    print("FD parsing done. Conversion to legacy internal representation...")

    predicates = DynamicList()

    for atom in atoms:
        predicate = normalize_atom(atom)
        predicates.add(predicate)

    action_to_op_id = {}
    op_id_to_action = {}
    op_id_to_operator = {}

    for action in actions:
        pre_pos = list(map(predicates.get_id, map(normalize_atom, action.precondition)))
        pre_neg = []
        eff_pos = list(map(predicates.get_id, map(lambda x: normalize_atom(x[1]), action.add_effects)))
        eff_neg = list(map(predicates.get_id, map(lambda x: normalize_atom(x[1]), action.del_effects)))

        operator = Operator(action.name, pre_pos, pre_neg, eff_pos, eff_neg)
        op_id = len(action_to_op_id)

        action_to_op_id[action.name] = op_id
        op_id_to_action[op_id] = action.name
        op_id_to_operator[op_id] = operator

    # print('\n'.join(predicate_to_var_id))

    init_pos = list(map(lambda x: predicates.get_id(normalize_atom(x)), task.init))
    init_neg = []
    goal_pos = list(map(lambda x: predicates.get_id(normalize_atom(x)), task.goal.to_untyped_strips()))
    goal_neg = []

    problem = StripsProblem(predicates.dic, predicates.reverse_dic,
                            action_to_op_id, op_id_to_action,
                            op_id_to_operator,
                            init_pos, init_neg,
                            goal_pos, goal_neg)

    print(f"Done. Found {problem.get_fluent_count()} fluents and {problem.get_operator_count()} operators "
          f"in {perf_counter() - global_start:.1f}s")
    step_time = perf_counter() - global_start  # Remove
    print(f"Conversion to STRIPS done in {step_time:.1f}s!")

    return problem


def normalize_atom(atom):
    return str(atom)[5:]


class DynamicList:
    def __init__(self):
        self.dic = {}
        self.reverse_dic = {}

    def add(self, item):
        self.get_id(item)

    def get_id(self, item):
        if item in self.dic:
            return self.dic[item]

        self.dic[item] = len(self.dic)
        self.reverse_dic[self.dic[item]] = item
        return self.dic[item]
