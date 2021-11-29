from antlr.PddlListener import PddlListener
from collections import namedtuple
from itertools import islice
from ASTypes import *


class InstanceListener(PddlListener):

    def __init__(self):
        self.pddlInstance = None

        self.name = ""
        self.objects = {'UNTYPED': []}

        self.initPredicates = []
        self.goalPredicates = []

        self.currentlyParsing = None  # 'Goal', 'Objects' or None

    def buildStructure(self):
        self.pddlInstance = PDDLInstance(self.name, self.objects,
                                         self.initPredicates,
                                         self.goalPredicates)

    # Initial state parsing methods
    def enterInit_(self, ctx):
        self.currentlyParsing = "Init"

    def exitInit_(self, ctx):
        self.currentlyParsing = None

    def enterInitEl(self, ctx):
        nameLiteral = ctx.nameLiteral()
        nameLiteralChildren = list(nameLiteral.getChildren())

        if len(nameLiteralChildren) >= 1:
            atomicNameFormula = nameLiteral.atomicNameFormula()
            predicate = f"({atomicNameFormula.predicate().getText()} {' '.join(map(str, atomicNameFormula.NAME()))})"
            hashedLiteral = HashedLiteral('+', predicate)

            if len(nameLiteralChildren) > 1 and nameLiteralChildren[1] == 'not':
                hashedLiteral.sign = '-'

            self.initPredicates.append(hashedLiteral)

    # Goal state parsing
    def enterGoal(self, ctx):
        self.currentlyParsing = 'Goal'

    def exitGoal(self, ctx):
        self.currentlyParsing = None

    def enterGoalDesc(self, ctx):
        children = list(ctx.getChildren())
        if len(children) == 1:
            # In this case, we have a single atom
            self.parseLiteral(ctx)

        elif len(children) > 1:
            # In this case, we have a multi-variable operator, and we assume
            # that it is only a conjunction of goals
            if children[1].getText().lower() == 'and':
                # We assume that at this point, we are given a literal, i.e.,
                # there are no complex goal
                for literal in ctx.goalDesc():
                    self.parseLiteral(literal)

    def parseLiteral(self, literal):
        """
        Add in the goalPredicates list the literal that is encoded in the argument

        Args:
            - literal: A goalDesc object that is expected to represent either a
                negated predicate, or a predicate
        """
        atomicTermFormula = None

        sign = '+'
        literalChildren = list(literal.getChildren())
        if len(literalChildren) > 1 and literalChildren[1].getText() == 'not':
            sign = '-'
            try:
                atomicTermFormula = literal.goalDesc().atomicTermFormula()
            except:
                print("Error: goal formula too complex")
        else:
            atomicTermFormula = literal.atomicTermFormula()

        predicateName = atomicTermFormula.predicate()
        args = atomicTermFormula.term()

        # NOTE: .lower() is a temporary fix
        hashedPredicate = f"({predicateName.getText().lower()} {' '.join(map(lambda x: x.getText(), args))})"
        hashedLiteral = HashedLiteral(sign, hashedPredicate)

        self.goalPredicates.append(hashedLiteral)

    # Problem name parsing
    def enterProblemDecl(self, ctx):
        self.name = ctx.NAME()
        print(f"Started to parse instance {ctx.NAME()}")

    # Instance-specific objects parsing
    def enterObjectDecl(self, ctx):
        self.currentlyParsing = 'Objects'
        # typed_objects_list = next(islice(ctx.getChildren(), 2, None)).getChildren()
        # for child in typed_objects_list:
        #      self.objects["UNTYPED"].append(child.getText())

    def exitObjectDecl(self, ctx):
        self.currentlyParsing = None

    def enterTypedNameList(self, ctx):
        if self.currentlyParsing != 'Objects':
            return
        for child in ctx.NAME():
            self.objects["UNTYPED"].append(child.getText())

    def enterSingleTypeNameList(self, ctx):
        if self.currentlyParsing != 'Objects':
            return
        object_type = ctx.t.getText()
        for child in ctx.NAME():
            if object_type in self.objects:
                self.objects[object_type].append(child.getText())
            else:
                self.objects[object_type] = [child.getText()]

    def getObjects(self):
        return self.objects

    def getPDDLStructure(self):
        return self.pddlInstance
