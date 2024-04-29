import pytest


# available only in same module, or from conftest.py
@pytest.fixture
def supply_AA_BB_CC():
    aa = 25
    bb = 35
    cc = 45
    return [aa, bb, cc]


def test_compareWithAA(supply_AA_BB_CC):
    zz = 35
    assert supply_AA_BB_CC[0] == zz


def test_compareWithBB(supply_AA_BB_CC):
    zz = 35
    assert supply_AA_BB_CC[1] == zz


def test_compareWithCC(supply_AA_BB_CC):
    zz = 35
    assert supply_AA_BB_CC[2] == zz


# auto import from conftest in this or parent folder


def test_compareWithAA_conftest_local(supply_AA_BB_CC_conftest_local):
    zz = 185
    assert supply_AA_BB_CC_conftest_local[0] == zz


def test_compareWithBB_conftest_local(supply_AA_BB_CC_conftest_local):
    zz = 185
    assert supply_AA_BB_CC_conftest_local[1] == zz


def test_compareWithCC_conftest_local(supply_AA_BB_CC_conftest_local):
    zz = 185
    assert supply_AA_BB_CC_conftest_local[2] == zz
