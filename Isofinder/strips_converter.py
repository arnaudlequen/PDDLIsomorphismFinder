from parser.instance_listener import InstanceListener
from parser.domain_listener import DomainListener
from parser.ast_types import PDDLDomain, PDDLInstance
from antlr.PddlLexer import PddlLexer, FileStream, CommonTokenStream
from antlr.PddlParser import PddlParser, ParseTreeWalker
from grounder import *


class StripsConverter:
    def __init__(self):
        # PDDL problems
        self.domains = []
        self.instances = []
        # STRIPS problems
        self.problems = []

        self.grounder = Grounder()

    @staticmethod
    def build_from_file(path, listener):
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

    def build_domain(self, path) -> PDDLDomain:
        pddl_domain = self.build_from_file(path, DomainListener)
        self.domains.append(pddl_domain)

        return pddl_domain

    def build_instance(self, path) -> PDDLInstance:
        pddl_instance = self.build_from_file(path, InstanceListener)
        self.instances.append(pddl_instance)

        return pddl_instance

    def build_strips_problem(self, domain, instance) -> StripsProblem:
        """
        Ground the instance using the appropriate domain

        Args:
            domain: A PDDLDomain
            instance: A PDDLInstance

        Return:
            problem: A StripsProblem problem that corresponds to the STRIPS problem encoded in (domain, instance)
        """
        problem = self.grounder.ground_instance(domain, instance)
        self.problems.append(problem)

        return problem

    def get_last_domain(self) -> PDDLDomain:
        return self.domains[-1]

    def get_last_instance(self) -> PDDLInstance:
        return self.instances[-1]
