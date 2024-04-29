def test_compareWithAA_conftest(supply_AA_BB_CC_conftest):
    zz = 85
    assert supply_AA_BB_CC_conftest[0] == zz


def test_compareWithBB_conftest(supply_AA_BB_CC_conftest):
    zz = 85
    assert supply_AA_BB_CC_conftest[1] == zz


def test_compareWithCC_conftest(supply_AA_BB_CC_conftest):
    zz = 85
    assert supply_AA_BB_CC_conftest[2] == zz


# won't load this fixture: it's in another module, not in this module or in coftest


def test_compareWithAA(supply_AA_BB_CC):
    zz = 35
    assert supply_AA_BB_CC[0] == zz


def test_compareWithBB(supply_AA_BB_CC):
    zz = 35
    assert supply_AA_BB_CC[1] == zz


def test_compareWithCC(supply_AA_BB_CC):
    zz = 35
    assert supply_AA_BB_CC[2] == zz
