import os

import pytest

from mytb.exceptions import MyTBError
from mytb.path import robust_makedirs


def test_robust_makedirs(tmp_path, monkeypatch):

    # create new dir and check no fail if existing
    dir1 = str(tmp_path / "d1" / "d2")
    robust_makedirs(dir1)
    assert os.path.isdir(dir1), "can create non existing dir"
    robust_makedirs(dir1)
    assert os.path.isdir(dir1), "pass on existing dir"

    dir2 = os.path.join(dir1, "f3")
    dir3 = os.path.join(dir2, "d4")
    with open(dir2, "w"):  # create empty file
        pass

    # can't create a directory on top of an existing file
    with pytest.raises(MyTBError):
        robust_makedirs(dir2)

    # can't create a directory below a file
    with pytest.raises(OSError):
        robust_makedirs(dir3)

    orig_mkdirs = os.makedirs
    dir4 = str(tmp_path / "d2" / "d3")

    def mymkdirs(path, *args, **kwargs):
        orig_mkdirs(path)
        if path == dir4:  # makedirs is recursive, so raise only for dir4
            raise OSError("can't create directory, it exists already")

    monkeypatch.setattr(os, "makedirs", mymkdirs)
    robust_makedirs(dir4)
    assert os.path.isdir(dir4), "pass on dir created while trying"
