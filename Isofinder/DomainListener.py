from antlr.PddlListener import PddlListener
from antlr.PddlParser import *
from collections import namedtuple
import itertools as it
from ASTypes import *


class DomainListener(PddlListener):

    def __init__(self):
        self.pddlDomain = None

        self.name = ""
        self.predicates = []
        self.actions = []

    def buildStructure(self):
        self.pddlDomain = PDDLDomain(self.name, self.predicates, self.actions)

    def enterDomainName(self, ctx):
        self.name = ctx.NAME()

    def enterAtomicFormulaSkeleton(self, ctx):
        """
        Parse the predicates. Can be done like this because the rule atomicFormulaSkeleton can only be applied in the
        case where we are parsing a predicate
        """
        name = ctx.predicate().getText()

        # TEMPORARY - only works for non-typed domains
        arguments_type_list = []
        typedVariableList = ctx.typedVariableList()
        for singleTypeVarList in typedVariableList.singleTypeVarList():
            object_type = singleTypeVarList.t.getText()
            arguments_type_list.extend([object_type] * len(singleTypeVarList.VARIABLE()))

        arguments_type_list.extend(["UNTYPED"] * len(typedVariableList.VARIABLE()))

        predicate = Predicate(name, arguments_type_list)

        self.predicates.append(predicate)

    def enterActionDef(self, ctx):
        """
        Parse the actions of the problem
        """
        action_name = next(it.islice(ctx.getChildren(), 2, None)).getText()
        parameters_raw = next(it.islice(ctx.getChildren(), 5, None))
        actionDefBody = next(it.islice(ctx.getChildren(), 7, None))

        parameters = {}

        # Retrieve the parameters and their respective types
        # Start by finding the types of each parameters
        if parameters_raw.VARIABLE():
            parameters["UNTYPED"] = []

        for variable in parameters_raw.VARIABLE():
            parameters["UNTYPED"].append(variable.getText())

        for singleTypeVarList in parameters_raw.singleTypeVarList():
            objects_type = singleTypeVarList.t.getText()
            if objects_type not in parameters:
                parameters[objects_type] = []

            for variable in singleTypeVarList.VARIABLE():
                parameters[objects_type].append(variable.getText())

        # Build the reverse association table for convenience
        variable_to_type = {}

        for variable_type, variable_list in parameters.items():
            for variable in variable_list:
                variable_to_type[variable] = variable_type

        # Then explore the actions, but without the proper types (as types are given in the parameters only)
        precondition_raw = next(it.islice(actionDefBody.getChildren(), 1, None))
        effects_raw = next(it.islice(actionDefBody.getChildren(), 3, None))

        precondition = self.exploreAction(precondition_raw)
        effects = self.exploreAction(effects_raw)

        # Affect the correct type to each symbol of the preconditions and effects
        for literal in it.chain(precondition, effects):
            old_action_predicate = literal.predicate
            new_arguments_type_list = []
            for argument_name in old_action_predicate.arguments_name_list:
                new_arguments_type_list.append(variable_to_type[argument_name])
            old_action_predicate.arguments_type_list = new_arguments_type_list

        action = Action(action_name, parameters, precondition, effects)
        self.actions.append(action)

    def exploreAction(self, node):
        """
        Build the list of predicates that one can find in an action. Can handle both preconditions and effects.
        """
        # Exploration of the preconditions
        if isinstance(node, PddlParser.GoalDescContext):
            children = list(node.getChildren())
            if len(children) <= 1:
                # This should be an atomicTermFormula, and handled in another call
                assert isinstance(children[0], PddlParser.AtomicTermFormulaContext), "Unsupported precondition description"
                return [self.exploreAction(children[0])]
            else:
                if children[1].getText() == 'and':
                    # Return each of the subsequent predicates
                    preconds = it.filterfalse(lambda x: self.andFilter(x.getText()), node.getChildren())
                    found_predicates = []

                    for pre in preconds:
                        found_predicates.extend(self.exploreAction(pre))

                    return found_predicates

                elif children[1].getText() == 'not':
                    # We assume a very basic description of the preconditions
                    literal = self.exploreAction(children[2])
                    assert isinstance(literal, Literal), "Unsupported precondition description"
                    return Literal('-', literal.predicate)

        # Exploration of the effects
        elif isinstance(node, PddlParser.EffectContext):
            # print(f"Found effect: {node.getText()}")
            ceffects = it.filterfalse(lambda x: self.andFilter(x.getText()), node.getChildren())
            found_predicates = []

            for ceff in ceffects:
                found_predicates.append(self.exploreAction(ceff))

            return found_predicates

        elif isinstance(node, PddlParser.CEffectContext):
            children = list(node.getChildren())
            if len(children) > 1 or not isinstance(children[0], PddlParser.PEffectContext):
                return []
            return self.exploreAction(children[0])

        elif isinstance(node, PddlParser.PEffectContext):
            children = list(node.getChildren())

            if len(children) > 1:
                # We are in a negation. Process the "not", then go and find the underlying predicate
                assert children[1].getText() == "not", f"Unsupported operation (non-STRIPS): {children[1].getText()}"
                literal = self.exploreAction(children[2])
                assert isinstance(literal, Literal), f"Unsupported effect description"
                return Literal('-', literal.predicate)
            else:
                #Otherwise this is a predicate that we can return directly
                return self.exploreAction(children[0])

        # Base case
        elif isinstance(node, PddlParser.AtomicTermFormulaContext):
            # For some reason, there is an additional child
            child = node
            terms = list(it.filterfalse(lambda x: self.andFilter(x.getText()), child.getChildren()))
            arguments = list(map(lambda x: x.getText(), terms[1:]))
            action_predicate = ActionPredicate(terms[0].getText(), ["UNTYPED"]*len(arguments), arguments)
            return Literal('+', action_predicate)

    def andFilter(self, x):
        return x in ['(', ')', 'and']

    def getActions(self):
        return self.actions

    def getPredicates(self):
        return self.predicates

    def getPDDLStructure(self):
        return self.pddlDomain
