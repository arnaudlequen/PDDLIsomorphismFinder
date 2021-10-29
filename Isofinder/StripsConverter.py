import sys
from antlr4 import *
from antlr.PddlLexer import PddlLexer
from antlr.PddlParser import PddlParser
from DomainListener import *
from InstanceListener import *
from Grounder import *
from time import time

class StripsConverter:
    def __init__(self):
        # PDDL problems
        self.domains = []
        self.instances = []
        # STRIPS problems
        self.problems = []

        self.grounder = Grounder()

    def buildFromFile(self, path, listener):
        """
        Read a file and extract the semantic structure from it, using the appropriate listener
        """
        input_stream = FileStream(path)
        lexer = PddlLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = PddlParser(stream)

        tree = parser.pddlDoc()
        listener = listener()

        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        listener.buildStructure()

        return listener.getPDDLStructure()

    def buildDomain(self, path):
        pddlDomain = self.buildFromFile(path, DomainListener)
        self.domains.append(pddlDomain)

        return pddlDomain

    def buildInstance(self, path):
        pddlInstance = self.buildFromFile(path, InstanceListener)
        self.instances.append(pddlInstance)

        return pddlInstance

    def buildStripsProblem(self, domain, instance):
        """
        Ground the instance using the appropriate domain

        Args:
            domain: A PDDLDomain
            instance: A PDDLInstance

        Return:
            problem: A StripsProblem problem that corresponds to the STRIPS problem encoded in (domain, instance)
        """
        problem = self.grounder.groundInstance(domain, instance)
        self.problems.append(problem)

        return problem

    def getLastDomain(self):
        return self.domains[-1]

    def getLastInstance(self):
        return self.instances[-1]
