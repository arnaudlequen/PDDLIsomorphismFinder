from collections import namedtuple

"""
Predicate

A tuple that consists of the name and the types of the arguments of a predicate
"""
Predicate = namedtuple('Predicate', ['name', 'arguments_type_list'])

"""
ActionPredicate

A tuple that consists of an open predicate of the like one may find in actions. The difference with the previous
definition of predicate is that the arguments are named, which allows for unification with other predicates
"""
ActionPredicate = namedtuple('ActionPredicate', ['name', 'arguments_type_list', 'arguments_name_list'])

"""
Literal

A predicate that can be either positive or negative

Args:
    sign: The string value '+' or '-', which represents whether the predicate is positive or negative
    predicate: Either a Predicate or an ActionPredicate
"""
Literal = namedtuple('Literal', ['sign', 'predicate']) # sign should be + or -

"""
HashedLiteral

A hashed, grounded predicate that can be either positive or negative

Args:
    sign: The string value '+' or '-', which represents whether the predicate is positive or negative
    predicate: A string that represents a predicate
"""
HashedLiteral = namedtuple('HashedPredicate', ['sign', 'predicate'])

#
# PDDL types
#
"""
PDDLDomain

A structure that represents a PDDLDomain that has been extracted from the domain file

Args:
    name: The name of the domain
    predicates: A list of predicates
"""
PDDLDomain = namedtuple('PDDLDomain', ['name', 'predicates', 'actions'])

"""
PDDLInstance

A structure that represents a PDDL instance that has been extracted from a problem file
"""
PDDLInstance = namedtuple('PDDLInstance', ['name', 'objects', 'init', 'goal'])


"""
Action

An action found a PDDL instance

Args:
    name: The name of the action
    parameters: A dictionary where keys are types and values are lists of symbols of a certain type
    precondition: A list of Literals, where predicate is an ActionPredicate
    effects: A list of Literals, where predicate is an ActionPredicate

"""
Action = namedtuple('Action', ['name', 'parameters', 'precondition', 'effects'])

#
# STRIPS types
#
"""
Operator

An operator fonud in a STRIPS instance

Args:
    name: The name of the operator
    pre_pos: A list of int, which are the ids of the variables associated to some fluents. Represents the positive preconditions
    pre_neg: A list of int, which are the ids of the variables associated to some fluents. Represents the negative preconditions
    eff_pos: A list of int, which are the ids of the variables associated to some fluents. Represents the add effects
    eff_neg: A list of int, which are the ids of the variables associated to some fluents. Represents the delete effects
"""
Operator = namedtuple('Operator', ['name', 'pre_pos', 'pre_neg', 'eff_pos', 'eff_neg'])
