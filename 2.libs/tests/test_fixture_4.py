def test_compareWithAA(supply_AA_BB_CC_conftest_to_out_of_package):
    zz = 285
    assert supply_AA_BB_CC_conftest_to_out_of_package[0] == zz


def test_compareWithBB(supply_AA_BB_CC_conftest_to_out_of_package):
    zz = 285
    assert supply_AA_BB_CC_conftest_to_out_of_package[1] == zz


def test_compareWithCC(supply_AA_BB_CC_conftest_to_out_of_package):
    zz = 285
    assert supply_AA_BB_CC_conftest_to_out_of_package[2] == zz
