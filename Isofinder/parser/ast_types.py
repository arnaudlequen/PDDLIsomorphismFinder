from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Predicate:
    """
    Predicate

    A structure that consists of the name and the types of the arguments of a predicate

    Attributes:
        name (str): The symbol that represents the predicate
        arguments_type_list (list): The sequence of types
    """
    name: str
    arguments_type_list: list


@dataclass
class ActionPredicate(Predicate):
    """
    ActionPredicate

    A structure that consists of an open predicate of the like one may find in actions. The difference with the previous
    definition of predicate is that the arguments are named, which allows for unification with other predicates

    Attributes:
        arguments_name_list (List[str]): The sequence of symbols that represent the arguments
    """
    arguments_name_list: List[str]


@dataclass
class Literal:
    """
    Literal

    A predicate that can be either positive or negative

    Attributes:
        sign: The string value '+' or '-', which represents whether the predicate is positive or negative
        predicate: Either a Predicate or an ActionPredicate
    """
    sign: str
    predicate: Predicate


@dataclass
class HashedLiteral:
    """
    HashedLiteral

    A hashed, grounded predicate that can be either positive or negative

    Attributes:
        sign: The string value '+' or '-', which represents whether the predicate is positive or negative
        predicate: A string that represents a predicate
    """
    sign: str
    predicate: Predicate


#
# PDDL types
#
@dataclass
class PDDLDomain:
    """
    PDDLDomain

    A structure that represents a PDDLDomain that has been extracted from the domain file

    Attributes:
        name: The name of the domain
        predicates: A list of predicates
    """
    name: str
    predicates: List[Predicate]
    actions: List[ActionPredicate]


@dataclass
class PDDLInstance:
    """
    PDDLInstance

    A structure that represents a PDDL instance that has been extracted from a problem file
    """
    name: str
    objects: Dict[str, List]
    init: List[HashedLiteral]
    goal: List[HashedLiteral]


@dataclass
class Action:
    """
    Action

    An action found in a PDDL instance

    Attributes:
        name: The name of the action
        parameters: A dictionary where keys are types and values are lists of symbols of a certain type
        precondition: A list of Literals, where predicate is an ActionPredicate
        effects: A list of Literals, where predicate is an ActionPredicate

    """
    name: str
    parameters: dict
    precondition: List[Literal]
    effects: List[Literal]


#
# STRIPS types
#
@dataclass
class Operator:
    """
    Operator

    An operator found in a STRIPS instance

    Attributes:
        name: The name of the operator
        pre_pos (List[int]): The ids of the variables associated to some fluents. Represents the positive preconditions
        pre_neg (List[int]): The ids of the variables associated to some fluents. Represents the negative preconditions
        eff_pos (List[int]): The ids of the variables associated to some fluents. Represents the add effects
        eff_neg (List[int]): The ids of the variables associated to some fluents. Represents the delete effects
    """
    name: str
    pre_pos: List[int]
    pre_neg: List[int]
    eff_pos: List[int]
    eff_neg: List[int]
