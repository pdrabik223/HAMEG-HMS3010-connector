import pytest
from requests.utils import get_or_raise


class TestGetOrRaise:
    def test_get_or_raise_correct_input(self):
        assert get_or_raise(4, int) == 4
        assert get_or_raise(4.3, float) == 4.3

        assert type(get_or_raise(12, float)) == float
        assert get_or_raise(12, float) == 12.0

        assert type(get_or_raise(4.5, int)) == int
        assert get_or_raise(4.5, int) == 4

        assert get_or_raise("4", int) == 4
        assert get_or_raise("12.7", float) == 12.7

    def test_get_or_raise_error(self):
        with pytest.raises(TypeError) as ex:
            get_or_raise("str", int, "val")
            get_or_raise(None, int, "val")
