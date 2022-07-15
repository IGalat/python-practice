from hypothesis import given
from hypothesis.strategies import sampled_from

from key import Keys, Key
from util.misc import enum_to_dict


class TestKeys:
    @given(sampled_from(Keys))
    def test_hypoExistingCodes_by_vk_code(self, key: Key) -> None:
        vk = key.vk_code
        if vk is None:
            assert not Keys.by_vk_code(vk)
        else:
            assert key == Keys.by_vk_code(vk)

    @given(sampled_from(list(enum_to_dict(Keys).keys())))
    def test_hypoKeyNames_by_str(self, name: str) -> None:
        assert Keys[name] == Keys.by_str(name)
