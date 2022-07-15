import pytest


@pytest.fixture
def supply_AA_BB_CC_conftest_local():
    aa = 175
    bb = 185
    cc = 195
    return [aa, bb, cc]


# from coftest - not available in parent folder


@pytest.fixture
def supply_AA_BB_CC_conftest_to_out_of_package():
    aa = 275
    bb = 285
    cc = 295
    return [aa, bb, cc]


# has to be exported manually


external_conditional_skip_marker = pytest.mark.skipif("qua" == "linux", reason="does not run on linux")
