import pytest


# from coftest - available in folder and subfolders


@pytest.fixture
def supply_AA_BB_CC_conftest():
    aa = 75
    bb = 85
    cc = 95
    return [aa, bb, cc]
