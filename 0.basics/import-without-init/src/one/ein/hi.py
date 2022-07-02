from one.uno import hi_sp as spanish


def hi_german() -> str:
    return "Guten tag"


def hi_both() -> str:
    return spanish.hi_spanish() + " " + hi_german()
