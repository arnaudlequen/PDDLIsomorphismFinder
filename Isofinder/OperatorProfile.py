import attr


@attr.s(slots=True)
class OperatorProfile:
    # Size of the different attributes
    pre_pos: int = attr.ib(default=-1)
    pre_neg: int = attr.ib(default=-1)
    eff_pos: int = attr.ib(default=-1)
    eff_neg: int = attr.ib(default=-1)

    # Compare variables seed in two different attributes of the operator
    # Number of vars in pre^+ found in eff^-
    prep_to_effn: int = attr.ib(default=-1)
    pren_to_effp: int = attr.ib(default=-1)




