from antlr.PddlListener import PddlListener
from collections import namedtuple
from itertools import islice
from ASTypes import *


class InstanceListener(PddlListener):

    def __init__(self):
        self.pddlInstance = None

        self.name = ""
        self.objects = {'UNTYPED': []}

    def buildStructure(self):
        self.pddlInstance = PDDLInstance(self.name, self.objects)

    def enterProblemDecl(self, ctx):
        self.name = ctx.NAME()
        print(f"Started to parse instance {ctx.NAME()}")

    def enterObjectDecl(self, ctx):
        typed_objects_list = next(islice(ctx.getChildren(), 2, None)).getChildren()
        for child in typed_objects_list:
            self.objects["UNTYPED"].append(child.getText())

    def getObjects(self):
        return self.objects

    def getPDDLStructure(self):
        return self.pddlInstance
