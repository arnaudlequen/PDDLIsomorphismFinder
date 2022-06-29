from parser.ast_types import Operator
import itertools as it

filler = ''.join(['='] * 30)
small_filler = ''.join(['-'] * 30)


def verify_homomorphism(problem1, problem2, args):
    print("Verifying embedding...")
    print(filler)
    f_map = {}  # F' -> F
    o_map = {}  # O  -> O'

    errors = set()
    skip = False  # When a crucial property is not respected, we have to skip some tests

    print("Mapping definition... ", end='')
    errors_len = len(errors)
    mode = None
    with open(args.output, 'r') as hfile:
        for raw_line in hfile.readlines():
            line = raw_line.rstrip('\n')
            if line.startswith('=============================='):
                continue
            elif line.startswith("FLUENTS"):
                mode = 'fluents'
            elif line.startswith("OPERATORS"):
                mode = 'operators'
            elif len(line) > 0:
                if mode == 'fluents':
                    f1_id, f2_id = parse_fluent(problem1, problem2, line)
                    # Check that the mapping is correct
                    if f2_id in f_map:
                        errors.add(f"Fluent mapping not correct: multiple values "
                                   f"for {problem2.get_fluent_name(f2_id)} in F'")
                        skip = True
                    f_map[f2_id] = f1_id
                elif mode == 'operators':
                    o1_id, o2_id = parse_operator(problem1, problem2, line)
                    if o1_id in o_map:
                        skip = True
                        errors.add(f'Operator mapping not correct: multiple values '
                                   f'for {problem1.get_operator_by_id(o1_id).name} in O')
                    o_map[o1_id] = o2_id
    print(new_errors(errors, errors_len))

    # Verify that all elements of F' have an image
    print("Completude of fluents mapping... ", end='')
    errors_len = len(errors)
    if len(f_map) < problem2.get_fluent_count():
        errors.add("Mapping u: F' -> F partial, some fluents left unmapped")
        skip = True
    print(new_errors(errors, errors_len))

    # Verify that all elements of O have an image
    print("Completude of operators mapping... ", end='')
    errors_len = len(errors)
    if len(o_map) < problem1.get_operator_count():
        errors.add("Mapping v: O -> O' partial, some operators left unmapped")
        skip = True
    print(new_errors(errors, errors_len))

    # Verify that the fluent mapping is injective
    print("Injectivity of fluent mapping... ", end='')
    errors_len = len(errors)
    if not skip:
        image_fluents = set()
        for f1_id in f_map.values():
            if f1_id in image_fluents:
                errors.add(f"Fluent {f1_id} in F image of multiple fluents of F'")
            image_fluents.add(f1_id)
    print(new_errors(errors, errors_len, skip))

    # Check the morphism property
    print("Homomorphism property... ", end='')
    errors_len = len(errors)
    if not skip:
        for op1 in problem1.get_operators():
            active = False
            for f1_id in it.chain(op1.eff_pos, op1.eff_neg):
                if f1_id in image_fluents:
                    active = True
                    break
            if not active:
                continue

            # Check that u(S(v(o))) included in S(o) inter u(F')
            for rel in [lambda x: x.eff_pos, lambda x: x.eff_neg, lambda x: x.pre_pos]:
                op2 = problem2.get_operator_by_id(o_map[problem1.get_operator_id_by_name(op1.name)])
                for f2_id in rel(op2):
                    if f_map[f2_id] not in rel(op1):
                        errors.add(f"Morphism property not satisfied for operator {op1.name} -> {op2.name}")
                        break

            # Check the converse
            for rel in [lambda x: x.eff_pos, lambda x: x.eff_neg]:
                op2 = problem2.get_operator_by_id(o_map[problem1.get_operator_id_by_name(op1.name)])
                op2_rel_fluents = {f_map[f2_id] for f2_id in rel(op2)}
                for f1_id in rel(op1):
                    if f1_id not in op2_rel_fluents:
                        errors.add(f"Morphism property not satisfied for operator {op1.name} -> {op2.name}")
    print(new_errors(errors, errors_len, skip))

    # Check that goal fluents are conserved
    print("Goal fluents conservation... ", end='')
    errors_len = len(errors)
    if not skip:
        goal2_images = {f_map[f2_id] for f2_id in problem2.goal_pos}
        goal1_intersect = {f1_id for f1_id in problem1.goal_pos if f1_id in image_fluents}
        for f1_id in goal2_images:
            if f1_id not in goal1_intersect:
                errors.add(f"Fluent {f1_id} in u(G') but not a useful fluent of G")
    print(new_errors(errors, errors_len, skip))

    # Check that initial fluents are conserved
    print("Initial fluents conservation... ", end='')
    errors_len = len(errors)
    if not skip:
        init2_images = {f_map[f2_id] for f2_id in problem2.init_pos}
        init1_intersect = {f1_id for f1_id in problem1.init_pos if f1_id in image_fluents}
        for f1_id in init1_intersect:
            if f1_id not in init2_images:
                errors.add(f"Fluent {f1_id} useful and in I but not in u(I')")
    print(new_errors(errors, errors_len, skip))

    print(small_filler)
    print("All checks done: ", end='')
    if not errors:
        print("EMBEDDING CORRECT")
    else:
        print(f"{len(errors)} ERRORS FOUND")
        print('\n'.join(list(map(lambda x: '- ' + x, errors))))


def parse_fluent(problem1, problem2, line):
    f1_str, f2_str = line.split(' => ')
    f1_id = problem1.get_var_id_by_predicate(f1_str)
    f2_id = problem2.get_var_id_by_predicate(f2_str)

    return f1_id, f2_id


def parse_operator(problem1, problem2, line):
    o1_str, o2_str = line.split(' => ')
    o1_name = o1_str.split(':')[0][1:]
    o2_name = o2_str.split(':')[0][1:]
    o1_id = problem1.get_operator_id_by_name(o1_name)
    o2_id = problem2.get_operator_id_by_name(o2_name)

    return o1_id, o2_id


def new_errors(errors, err_len, skip=False):
    if skip:
        return 'skip'
    if len(errors) == err_len:
        return 'ok'
    return 'error'
