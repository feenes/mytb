#!/usr/bin/env python
# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.os
#
# Description:  os helpers
#
# #############################################################################

from __future__ import absolute_import, print_function

import os
import sys


_RELEASE = None  # well, OS version just has to be determined once


def is_windows(min_release=None, max_release=None):
    """ True if OS is WINDOWS  (between min / max_release) """
    global _RELEASE

    if sys.platform != 'win32':
        return False

    if _RELEASE is None:
        _RELEASE = sys.platform.release()

    if min_release is not None and int(_RELEASE) < min_release:
        return False

    if max_release is not None and int(_RELEASE) > max_release:
        return False

    return True


def is_linux():
    """ True if OS is linux """
    return sys.platform.startswith('linux')


def is_posix():
    """ True if OS is posix """
    return os.name == 'posix'


def is_macos_x():
    """ True if OS is mac """
    return sys.platform == 'darwin'


def is_cygwin():
    """ True if OS is cygwin """
    return sys.platform == 'cygwin'


def is_win_7():
    """ True if OS is windows 7 """
    return is_windows() and _RELEASE == '7'


def is_win_8():
    """ True if OS is windows 8 """
    return is_windows() and _RELEASE == '8'


def is_win_10():
    """ True if OS is windows 10 """
    return is_windows() and _RELEASE == '10'
