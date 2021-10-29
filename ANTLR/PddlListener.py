# Generated from Pddl.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .PddlParser import PddlParser
else:
    from PddlParser import PddlParser

# This class defines a complete listener for a parse tree produced by PddlParser.
class PddlListener(ParseTreeListener):

    # Enter a parse tree produced by PddlParser#pddlDoc.
    def enterPddlDoc(self, ctx:PddlParser.PddlDocContext):
        pass

    # Exit a parse tree produced by PddlParser#pddlDoc.
    def exitPddlDoc(self, ctx:PddlParser.PddlDocContext):
        pass


    # Enter a parse tree produced by PddlParser#domain.
    def enterDomain(self, ctx:PddlParser.DomainContext):
        pass

    # Exit a parse tree produced by PddlParser#domain.
    def exitDomain(self, ctx:PddlParser.DomainContext):
        pass


    # Enter a parse tree produced by PddlParser#domainName.
    def enterDomainName(self, ctx:PddlParser.DomainNameContext):
        pass

    # Exit a parse tree produced by PddlParser#domainName.
    def exitDomainName(self, ctx:PddlParser.DomainNameContext):
        pass


    # Enter a parse tree produced by PddlParser#requireDef.
    def enterRequireDef(self, ctx:PddlParser.RequireDefContext):
        pass

    # Exit a parse tree produced by PddlParser#requireDef.
    def exitRequireDef(self, ctx:PddlParser.RequireDefContext):
        pass


    # Enter a parse tree produced by PddlParser#typesDef.
    def enterTypesDef(self, ctx:PddlParser.TypesDefContext):
        pass

    # Exit a parse tree produced by PddlParser#typesDef.
    def exitTypesDef(self, ctx:PddlParser.TypesDefContext):
        pass


    # Enter a parse tree produced by PddlParser#typedNameList.
    def enterTypedNameList(self, ctx:PddlParser.TypedNameListContext):
        pass

    # Exit a parse tree produced by PddlParser#typedNameList.
    def exitTypedNameList(self, ctx:PddlParser.TypedNameListContext):
        pass


    # Enter a parse tree produced by PddlParser#singleTypeNameList.
    def enterSingleTypeNameList(self, ctx:PddlParser.SingleTypeNameListContext):
        pass

    # Exit a parse tree produced by PddlParser#singleTypeNameList.
    def exitSingleTypeNameList(self, ctx:PddlParser.SingleTypeNameListContext):
        pass


    # Enter a parse tree produced by PddlParser#type_.
    def enterType_(self, ctx:PddlParser.Type_Context):
        pass

    # Exit a parse tree produced by PddlParser#type_.
    def exitType_(self, ctx:PddlParser.Type_Context):
        pass


    # Enter a parse tree produced by PddlParser#primType.
    def enterPrimType(self, ctx:PddlParser.PrimTypeContext):
        pass

    # Exit a parse tree produced by PddlParser#primType.
    def exitPrimType(self, ctx:PddlParser.PrimTypeContext):
        pass


    # Enter a parse tree produced by PddlParser#functionsDef.
    def enterFunctionsDef(self, ctx:PddlParser.FunctionsDefContext):
        pass

    # Exit a parse tree produced by PddlParser#functionsDef.
    def exitFunctionsDef(self, ctx:PddlParser.FunctionsDefContext):
        pass


    # Enter a parse tree produced by PddlParser#functionList.
    def enterFunctionList(self, ctx:PddlParser.FunctionListContext):
        pass

    # Exit a parse tree produced by PddlParser#functionList.
    def exitFunctionList(self, ctx:PddlParser.FunctionListContext):
        pass


    # Enter a parse tree produced by PddlParser#atomicFunctionSkeleton.
    def enterAtomicFunctionSkeleton(self, ctx:PddlParser.AtomicFunctionSkeletonContext):
        pass

    # Exit a parse tree produced by PddlParser#atomicFunctionSkeleton.
    def exitAtomicFunctionSkeleton(self, ctx:PddlParser.AtomicFunctionSkeletonContext):
        pass


    # Enter a parse tree produced by PddlParser#functionSymbol.
    def enterFunctionSymbol(self, ctx:PddlParser.FunctionSymbolContext):
        pass

    # Exit a parse tree produced by PddlParser#functionSymbol.
    def exitFunctionSymbol(self, ctx:PddlParser.FunctionSymbolContext):
        pass


    # Enter a parse tree produced by PddlParser#functionType.
    def enterFunctionType(self, ctx:PddlParser.FunctionTypeContext):
        pass

    # Exit a parse tree produced by PddlParser#functionType.
    def exitFunctionType(self, ctx:PddlParser.FunctionTypeContext):
        pass


    # Enter a parse tree produced by PddlParser#constantsDef.
    def enterConstantsDef(self, ctx:PddlParser.ConstantsDefContext):
        pass

    # Exit a parse tree produced by PddlParser#constantsDef.
    def exitConstantsDef(self, ctx:PddlParser.ConstantsDefContext):
        pass


    # Enter a parse tree produced by PddlParser#predicatesDef.
    def enterPredicatesDef(self, ctx:PddlParser.PredicatesDefContext):
        pass

    # Exit a parse tree produced by PddlParser#predicatesDef.
    def exitPredicatesDef(self, ctx:PddlParser.PredicatesDefContext):
        pass


    # Enter a parse tree produced by PddlParser#atomicFormulaSkeleton.
    def enterAtomicFormulaSkeleton(self, ctx:PddlParser.AtomicFormulaSkeletonContext):
        pass

    # Exit a parse tree produced by PddlParser#atomicFormulaSkeleton.
    def exitAtomicFormulaSkeleton(self, ctx:PddlParser.AtomicFormulaSkeletonContext):
        pass


    # Enter a parse tree produced by PddlParser#predicate.
    def enterPredicate(self, ctx:PddlParser.PredicateContext):
        pass

    # Exit a parse tree produced by PddlParser#predicate.
    def exitPredicate(self, ctx:PddlParser.PredicateContext):
        pass


    # Enter a parse tree produced by PddlParser#typedVariableList.
    def enterTypedVariableList(self, ctx:PddlParser.TypedVariableListContext):
        pass

    # Exit a parse tree produced by PddlParser#typedVariableList.
    def exitTypedVariableList(self, ctx:PddlParser.TypedVariableListContext):
        pass


    # Enter a parse tree produced by PddlParser#singleTypeVarList.
    def enterSingleTypeVarList(self, ctx:PddlParser.SingleTypeVarListContext):
        pass

    # Exit a parse tree produced by PddlParser#singleTypeVarList.
    def exitSingleTypeVarList(self, ctx:PddlParser.SingleTypeVarListContext):
        pass


    # Enter a parse tree produced by PddlParser#constraints.
    def enterConstraints(self, ctx:PddlParser.ConstraintsContext):
        pass

    # Exit a parse tree produced by PddlParser#constraints.
    def exitConstraints(self, ctx:PddlParser.ConstraintsContext):
        pass


    # Enter a parse tree produced by PddlParser#structureDef.
    def enterStructureDef(self, ctx:PddlParser.StructureDefContext):
        pass

    # Exit a parse tree produced by PddlParser#structureDef.
    def exitStructureDef(self, ctx:PddlParser.StructureDefContext):
        pass


    # Enter a parse tree produced by PddlParser#actionDef.
    def enterActionDef(self, ctx:PddlParser.ActionDefContext):
        pass

    # Exit a parse tree produced by PddlParser#actionDef.
    def exitActionDef(self, ctx:PddlParser.ActionDefContext):
        pass


    # Enter a parse tree produced by PddlParser#actionSymbol.
    def enterActionSymbol(self, ctx:PddlParser.ActionSymbolContext):
        pass

    # Exit a parse tree produced by PddlParser#actionSymbol.
    def exitActionSymbol(self, ctx:PddlParser.ActionSymbolContext):
        pass


    # Enter a parse tree produced by PddlParser#actionDefBody.
    def enterActionDefBody(self, ctx:PddlParser.ActionDefBodyContext):
        pass

    # Exit a parse tree produced by PddlParser#actionDefBody.
    def exitActionDefBody(self, ctx:PddlParser.ActionDefBodyContext):
        pass


    # Enter a parse tree produced by PddlParser#goalDesc.
    def enterGoalDesc(self, ctx:PddlParser.GoalDescContext):
        pass

    # Exit a parse tree produced by PddlParser#goalDesc.
    def exitGoalDesc(self, ctx:PddlParser.GoalDescContext):
        pass


    # Enter a parse tree produced by PddlParser#fComp.
    def enterFComp(self, ctx:PddlParser.FCompContext):
        pass

    # Exit a parse tree produced by PddlParser#fComp.
    def exitFComp(self, ctx:PddlParser.FCompContext):
        pass


    # Enter a parse tree produced by PddlParser#atomicTermFormula.
    def enterAtomicTermFormula(self, ctx:PddlParser.AtomicTermFormulaContext):
        pass

    # Exit a parse tree produced by PddlParser#atomicTermFormula.
    def exitAtomicTermFormula(self, ctx:PddlParser.AtomicTermFormulaContext):
        pass


    # Enter a parse tree produced by PddlParser#term.
    def enterTerm(self, ctx:PddlParser.TermContext):
        pass

    # Exit a parse tree produced by PddlParser#term.
    def exitTerm(self, ctx:PddlParser.TermContext):
        pass


    # Enter a parse tree produced by PddlParser#durativeActionDef.
    def enterDurativeActionDef(self, ctx:PddlParser.DurativeActionDefContext):
        pass

    # Exit a parse tree produced by PddlParser#durativeActionDef.
    def exitDurativeActionDef(self, ctx:PddlParser.DurativeActionDefContext):
        pass


    # Enter a parse tree produced by PddlParser#daDefBody.
    def enterDaDefBody(self, ctx:PddlParser.DaDefBodyContext):
        pass

    # Exit a parse tree produced by PddlParser#daDefBody.
    def exitDaDefBody(self, ctx:PddlParser.DaDefBodyContext):
        pass


    # Enter a parse tree produced by PddlParser#daGD.
    def enterDaGD(self, ctx:PddlParser.DaGDContext):
        pass

    # Exit a parse tree produced by PddlParser#daGD.
    def exitDaGD(self, ctx:PddlParser.DaGDContext):
        pass


    # Enter a parse tree produced by PddlParser#prefTimedGD.
    def enterPrefTimedGD(self, ctx:PddlParser.PrefTimedGDContext):
        pass

    # Exit a parse tree produced by PddlParser#prefTimedGD.
    def exitPrefTimedGD(self, ctx:PddlParser.PrefTimedGDContext):
        pass


    # Enter a parse tree produced by PddlParser#timedGD.
    def enterTimedGD(self, ctx:PddlParser.TimedGDContext):
        pass

    # Exit a parse tree produced by PddlParser#timedGD.
    def exitTimedGD(self, ctx:PddlParser.TimedGDContext):
        pass


    # Enter a parse tree produced by PddlParser#timeSpecifier.
    def enterTimeSpecifier(self, ctx:PddlParser.TimeSpecifierContext):
        pass

    # Exit a parse tree produced by PddlParser#timeSpecifier.
    def exitTimeSpecifier(self, ctx:PddlParser.TimeSpecifierContext):
        pass


    # Enter a parse tree produced by PddlParser#interval.
    def enterInterval(self, ctx:PddlParser.IntervalContext):
        pass

    # Exit a parse tree produced by PddlParser#interval.
    def exitInterval(self, ctx:PddlParser.IntervalContext):
        pass


    # Enter a parse tree produced by PddlParser#derivedDef.
    def enterDerivedDef(self, ctx:PddlParser.DerivedDefContext):
        pass

    # Exit a parse tree produced by PddlParser#derivedDef.
    def exitDerivedDef(self, ctx:PddlParser.DerivedDefContext):
        pass


    # Enter a parse tree produced by PddlParser#fExp.
    def enterFExp(self, ctx:PddlParser.FExpContext):
        pass

    # Exit a parse tree produced by PddlParser#fExp.
    def exitFExp(self, ctx:PddlParser.FExpContext):
        pass


    # Enter a parse tree produced by PddlParser#fExp2.
    def enterFExp2(self, ctx:PddlParser.FExp2Context):
        pass

    # Exit a parse tree produced by PddlParser#fExp2.
    def exitFExp2(self, ctx:PddlParser.FExp2Context):
        pass


    # Enter a parse tree produced by PddlParser#fHead.
    def enterFHead(self, ctx:PddlParser.FHeadContext):
        pass

    # Exit a parse tree produced by PddlParser#fHead.
    def exitFHead(self, ctx:PddlParser.FHeadContext):
        pass


    # Enter a parse tree produced by PddlParser#effect.
    def enterEffect(self, ctx:PddlParser.EffectContext):
        pass

    # Exit a parse tree produced by PddlParser#effect.
    def exitEffect(self, ctx:PddlParser.EffectContext):
        pass


    # Enter a parse tree produced by PddlParser#cEffect.
    def enterCEffect(self, ctx:PddlParser.CEffectContext):
        pass

    # Exit a parse tree produced by PddlParser#cEffect.
    def exitCEffect(self, ctx:PddlParser.CEffectContext):
        pass


    # Enter a parse tree produced by PddlParser#pEffect.
    def enterPEffect(self, ctx:PddlParser.PEffectContext):
        pass

    # Exit a parse tree produced by PddlParser#pEffect.
    def exitPEffect(self, ctx:PddlParser.PEffectContext):
        pass


    # Enter a parse tree produced by PddlParser#condEffect.
    def enterCondEffect(self, ctx:PddlParser.CondEffectContext):
        pass

    # Exit a parse tree produced by PddlParser#condEffect.
    def exitCondEffect(self, ctx:PddlParser.CondEffectContext):
        pass


    # Enter a parse tree produced by PddlParser#binaryOp.
    def enterBinaryOp(self, ctx:PddlParser.BinaryOpContext):
        pass

    # Exit a parse tree produced by PddlParser#binaryOp.
    def exitBinaryOp(self, ctx:PddlParser.BinaryOpContext):
        pass


    # Enter a parse tree produced by PddlParser#binaryComp.
    def enterBinaryComp(self, ctx:PddlParser.BinaryCompContext):
        pass

    # Exit a parse tree produced by PddlParser#binaryComp.
    def exitBinaryComp(self, ctx:PddlParser.BinaryCompContext):
        pass


    # Enter a parse tree produced by PddlParser#assignOp.
    def enterAssignOp(self, ctx:PddlParser.AssignOpContext):
        pass

    # Exit a parse tree produced by PddlParser#assignOp.
    def exitAssignOp(self, ctx:PddlParser.AssignOpContext):
        pass


    # Enter a parse tree produced by PddlParser#durationConstraint.
    def enterDurationConstraint(self, ctx:PddlParser.DurationConstraintContext):
        pass

    # Exit a parse tree produced by PddlParser#durationConstraint.
    def exitDurationConstraint(self, ctx:PddlParser.DurationConstraintContext):
        pass


    # Enter a parse tree produced by PddlParser#simpleDurationConstraint.
    def enterSimpleDurationConstraint(self, ctx:PddlParser.SimpleDurationConstraintContext):
        pass

    # Exit a parse tree produced by PddlParser#simpleDurationConstraint.
    def exitSimpleDurationConstraint(self, ctx:PddlParser.SimpleDurationConstraintContext):
        pass


    # Enter a parse tree produced by PddlParser#durOp.
    def enterDurOp(self, ctx:PddlParser.DurOpContext):
        pass

    # Exit a parse tree produced by PddlParser#durOp.
    def exitDurOp(self, ctx:PddlParser.DurOpContext):
        pass


    # Enter a parse tree produced by PddlParser#durValue.
    def enterDurValue(self, ctx:PddlParser.DurValueContext):
        pass

    # Exit a parse tree produced by PddlParser#durValue.
    def exitDurValue(self, ctx:PddlParser.DurValueContext):
        pass


    # Enter a parse tree produced by PddlParser#daEffect.
    def enterDaEffect(self, ctx:PddlParser.DaEffectContext):
        pass

    # Exit a parse tree produced by PddlParser#daEffect.
    def exitDaEffect(self, ctx:PddlParser.DaEffectContext):
        pass


    # Enter a parse tree produced by PddlParser#timedEffect.
    def enterTimedEffect(self, ctx:PddlParser.TimedEffectContext):
        pass

    # Exit a parse tree produced by PddlParser#timedEffect.
    def exitTimedEffect(self, ctx:PddlParser.TimedEffectContext):
        pass


    # Enter a parse tree produced by PddlParser#fAssignDA.
    def enterFAssignDA(self, ctx:PddlParser.FAssignDAContext):
        pass

    # Exit a parse tree produced by PddlParser#fAssignDA.
    def exitFAssignDA(self, ctx:PddlParser.FAssignDAContext):
        pass


    # Enter a parse tree produced by PddlParser#fExpDA.
    def enterFExpDA(self, ctx:PddlParser.FExpDAContext):
        pass

    # Exit a parse tree produced by PddlParser#fExpDA.
    def exitFExpDA(self, ctx:PddlParser.FExpDAContext):
        pass


    # Enter a parse tree produced by PddlParser#problem.
    def enterProblem(self, ctx:PddlParser.ProblemContext):
        pass

    # Exit a parse tree produced by PddlParser#problem.
    def exitProblem(self, ctx:PddlParser.ProblemContext):
        pass


    # Enter a parse tree produced by PddlParser#problemDecl.
    def enterProblemDecl(self, ctx:PddlParser.ProblemDeclContext):
        pass

    # Exit a parse tree produced by PddlParser#problemDecl.
    def exitProblemDecl(self, ctx:PddlParser.ProblemDeclContext):
        pass


    # Enter a parse tree produced by PddlParser#problemDomain.
    def enterProblemDomain(self, ctx:PddlParser.ProblemDomainContext):
        pass

    # Exit a parse tree produced by PddlParser#problemDomain.
    def exitProblemDomain(self, ctx:PddlParser.ProblemDomainContext):
        pass


    # Enter a parse tree produced by PddlParser#objectDecl.
    def enterObjectDecl(self, ctx:PddlParser.ObjectDeclContext):
        pass

    # Exit a parse tree produced by PddlParser#objectDecl.
    def exitObjectDecl(self, ctx:PddlParser.ObjectDeclContext):
        pass


    # Enter a parse tree produced by PddlParser#init_.
    def enterInit_(self, ctx:PddlParser.Init_Context):
        pass

    # Exit a parse tree produced by PddlParser#init_.
    def exitInit_(self, ctx:PddlParser.Init_Context):
        pass


    # Enter a parse tree produced by PddlParser#initEl.
    def enterInitEl(self, ctx:PddlParser.InitElContext):
        pass

    # Exit a parse tree produced by PddlParser#initEl.
    def exitInitEl(self, ctx:PddlParser.InitElContext):
        pass


    # Enter a parse tree produced by PddlParser#nameLiteral.
    def enterNameLiteral(self, ctx:PddlParser.NameLiteralContext):
        pass

    # Exit a parse tree produced by PddlParser#nameLiteral.
    def exitNameLiteral(self, ctx:PddlParser.NameLiteralContext):
        pass


    # Enter a parse tree produced by PddlParser#atomicNameFormula.
    def enterAtomicNameFormula(self, ctx:PddlParser.AtomicNameFormulaContext):
        pass

    # Exit a parse tree produced by PddlParser#atomicNameFormula.
    def exitAtomicNameFormula(self, ctx:PddlParser.AtomicNameFormulaContext):
        pass


    # Enter a parse tree produced by PddlParser#goal.
    def enterGoal(self, ctx:PddlParser.GoalContext):
        pass

    # Exit a parse tree produced by PddlParser#goal.
    def exitGoal(self, ctx:PddlParser.GoalContext):
        pass


    # Enter a parse tree produced by PddlParser#probConstraints.
    def enterProbConstraints(self, ctx:PddlParser.ProbConstraintsContext):
        pass

    # Exit a parse tree produced by PddlParser#probConstraints.
    def exitProbConstraints(self, ctx:PddlParser.ProbConstraintsContext):
        pass


    # Enter a parse tree produced by PddlParser#prefConGD.
    def enterPrefConGD(self, ctx:PddlParser.PrefConGDContext):
        pass

    # Exit a parse tree produced by PddlParser#prefConGD.
    def exitPrefConGD(self, ctx:PddlParser.PrefConGDContext):
        pass


    # Enter a parse tree produced by PddlParser#metricSpec.
    def enterMetricSpec(self, ctx:PddlParser.MetricSpecContext):
        pass

    # Exit a parse tree produced by PddlParser#metricSpec.
    def exitMetricSpec(self, ctx:PddlParser.MetricSpecContext):
        pass


    # Enter a parse tree produced by PddlParser#optimization.
    def enterOptimization(self, ctx:PddlParser.OptimizationContext):
        pass

    # Exit a parse tree produced by PddlParser#optimization.
    def exitOptimization(self, ctx:PddlParser.OptimizationContext):
        pass


    # Enter a parse tree produced by PddlParser#metricFExp.
    def enterMetricFExp(self, ctx:PddlParser.MetricFExpContext):
        pass

    # Exit a parse tree produced by PddlParser#metricFExp.
    def exitMetricFExp(self, ctx:PddlParser.MetricFExpContext):
        pass


    # Enter a parse tree produced by PddlParser#conGD.
    def enterConGD(self, ctx:PddlParser.ConGDContext):
        pass

    # Exit a parse tree produced by PddlParser#conGD.
    def exitConGD(self, ctx:PddlParser.ConGDContext):
        pass



del PddlParser