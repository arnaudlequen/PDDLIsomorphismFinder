import argparse
import itertools as it
import random
import re
import sys
from enum import Enum

script_description = """Script to trim n random objects from a PDDL instance"""
# Important note: in instance.pddl, all predicates (init, goal, etc.) must be on their own lines


class State(Enum):
    NEUTRAL = 0
    START = 1
    OBJECTS = 2


def find_objects(instance_file):
    mode = State.START
    objects = {}

    # Find all objects in the instance file, by type
    objects_tmp = []
    for ln in instance_file.readlines():
        line = ln.strip()
        if ':objects' in line:
            mode = State.OBJECTS
            line = line.split(':objects')[-1]

        if mode == State.OBJECTS:
            objects_tmp += line.split()
            if line.endswith(')'):
                objects = process_obj_string(objects_tmp)
                return objects


def process_obj_string(objects_tmp):
    """
    Convert the raw list of elements found in list :objects to a dictionary of
    typed symbols lists
    """
    objects = {}

    last_cut = 0  # Index of the last item to be assigned in objects
    skip = False
    for i, obj in enumerate(objects_tmp):
        if skip:
            skip = False
            continue

        if obj == '-':
            if objects_tmp[i+1] in objects:
                objects[objects_tmp[i+1]].extend(objects_tmp[last_cut:i])
            else:
                objects[objects_tmp[i+1]] = objects_tmp[last_cut:i]
            last_cut = i+2

    if not objects:
        return {'UNTYPED': objects_tmp}

    return objects


def remove_objects(objects, n):
    sizes = {type: len(lst) for type, lst in objects.items()}
    removed_objects = {type: set() for type in objects.keys()}

    possible_choices = [type for type, size in sizes.items() if size > 1]

    for _ in range(n):
        if not possible_choices:
            break
        obj_type = random.choice(possible_choices)
        object = random.choice(
            list(set(objects[obj_type]).difference(removed_objects[obj_type])))
        removed_objects[obj_type].add(object)
        sizes[obj_type] -= 1
        if sizes[obj_type] <= 1:
            possible_choices.remove(obj_type)

    return removed_objects


def create_new_instance(instance, new_instance, removed_objects_flat):
    with open(instance, 'r+') as instance_file, \
            open(new_instance, 'w+') as new_instance_file:
        mode = State.NEUTRAL

        for ln in instance_file.readlines():
            line = ln.replace(')', ' ) ')
            new_line = ''

            if ':objects' in line:
                mode = State.OBJECTS

            if mode == State.OBJECTS:
                words = [word for word in line.split() if word not in removed_objects_flat]
                new_line = ' '.join(words) + '\n'
                if ')' in line:
                    mode = State.NEUTRAL

            elif mode == State.NEUTRAL:
                # Assuming one predicate per line at most
                if set(line.split()).intersection(removed_objects_flat):
                    new_line = ''
                else:
                    new_line = line

            new_instance_file.write(new_line)


def main(argv):
    parser = argparse.ArgumentParser(description=script_description)
    parser.add_argument('instance', metavar='instance.pddl', type=str,
                        help="Path to the instance of the form pXX.pddl to trim, with XX a double digit number")
    parser.add_argument('new_instance_path', metavar='new_instance_path',
                        type=str, help="Path to the new instance(s)")
    parser.add_argument('n', metavar='n', type=int,
                        help="Number of objects to remove", default=-1)
    parser.add_argument("-i", action=argparse.BooleanOptionalAction,
                        help="Interactively choose the fluents to remove")
    parser.add_argument('--chain', type=int, help='How many fluents to remove at each successive problem created, iteratively', default=0)
#    parser.add_argument('m', metavar='m', type=int, help='Step for chained problems', default=1)
    args = parser.parse_args()

    print('-'*24)
    print("STRIPS instance timmer")
    print('-'*24)
    print(f"Removing fluents from instance {args.instance}")
    print()

    print("Choosing fluents to remove...")
    print('='*24)
    with open(args.instance, 'r+') as instance_file:
        objects = find_objects(instance_file)
    if not args.i:
        removed_objects = remove_objects(objects, args.n)
        removed_objects_flat = set(it.chain(*[obj_list for obj_list in removed_objects.values()]))
    else:
        objects_flat = set(it.chain(*[obj_list for obj_list in objects.values()]))
        removed_objects_flat = []
        print(f"Choose a fluent to be removed ({args.n} to remove)")
        nb_fluents_to_remove = args.n
        while nb_fluents_to_remove > 0:
            symbol = input("> ")
            if symbol == '-1':
                break
            if symbol in objects_flat:
                removed_objects_flat.append(symbol)
                print(f"Fluent {symbol} added to remove list")
                nb_fluents_to_remove -= 1
            else:
                print("Object not found")


    print("Done. Fluents choosen:")
    print("> " + ', '.join(removed_objects_flat))
    print()

    print("Removing fluents...")
    print('='*24)
    if args.chain == 0:
        new_instance_number = int(re.findall(r'\d+', args.instance)[-1]) - args.n
        new_instance = f"pfile{new_instance_number}.pddl"
        create_new_instance(args.instance, new_instance, removed_objects_flat)
        print(f"Done. Output written in file {new_instance}")
    else:
        print("Creating multiple new instances...")
        instance_number = int(re.findall(r'\d+', args.instance)[-1])

        removed_objects_flat_list = list(removed_objects_flat)
        if not args.i:
            random.shuffle(removed_objects_flat_list)
        print(f"Order of removal: {', '.join(removed_objects_flat_list)}")

        if args.new_instance_path.endswith('/'):
            new_instance_path = args.new_instance_path
        else:
            new_instance_path = args.new_instance_path + '/'

        print("Writing output in files: ", end='')
        if args.chain != 0:
            rng = enumerate(range(instance_number - args.chain, instance_number - args.n - 1, -args.chain))
        else:
            rng = [(0, 1)]
        for i, new_instance_number in rng:
            new_instance = f"pfile{instance_number - i - 1}.pddl"
            save_path = new_instance_path + new_instance
            create_new_instance(args.instance, save_path, set(removed_objects_flat_list[:((i+1)*args.chain)]))
            print(f"{new_instance} ", end='')

        print()
        print("Done")

if __name__ == "__main__":
    main(sys.argv)
