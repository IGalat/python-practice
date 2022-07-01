import one.uno.hi as spanish


def hi_german():
    return "Guten tag"


def hi_both():
    return spanish.hi_spanish() + " " + hi_german()
