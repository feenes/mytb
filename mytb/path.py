from __future__ import absolute_import

import os

from mytb.exceptions import MyTBError


def robust_makedirs(path):
    """ create a directory in a robust race safe manner if not
        already existing.
        Good for multiprocessing / threading or cases where
        multiple actors might create a directory
    """
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except Exception:
            if not os.path.isdir(path):
                if os.path.isfile(path):
                    raise MyTBError("path %r is not a directory" % path)
                else:
                    raise
