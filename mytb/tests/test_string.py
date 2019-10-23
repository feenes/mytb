import pytest

from mytb.string import str2bool


class AClass(object):
    """ just a dummy type for testing """


def test_str2bool():
    # None should yield None
    assert str2bool(None) is None

    # some legal True strings, ints and floats
    for val in ("yes", "Yes", "TRUE", "y", "T", "1", 1, 2.):
        assert str2bool(val)

    # some legal False strings, ints and floats
    for val in ("nO", "False", "f", "N", "0", 0, 0., ""):
        assert str2bool(val) is False

    # unknwon strings and types shall raise an Exception
    for val in ("a", AClass()):
        with pytest.raises(ValueError):
            str2bool(val)
