#!/usr/bin/env python
# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.ipc.win_mutex
#
# Description:  mutex for windows os
#
# #############################################################################
from __future__ import absolute_import

import os

if os.name == 'win32':
    from win32event import CreateMutex
    from win32event import WaitForSingleObject
    from win32event import ReleaseMutex
    from win32api import GetLastError
    from winerror import ERROR_ALREADY_EXISTS


#                      76543210
TIMEOUT_INFINITE   = 0xffffffff  # noqa: E221
MTX_WAIT_ABANDONED = 0x00000080  # noqa: E221
MTX_WAIT_OBJECT_O  = 0x00000000  # noqa: E221
MTX_WAIT_TIMEOUT   = 0x00000102  # noqa: E221
MTX_WAIT_FAILED    = 0xffffffff  # noqa: E221


class IPCMutexError(Exception):
    """ Errors Specific to this module """


class IPCMutex(object):
    """ Basic wrapper around windows Named mutex object
        due to legacy reasons there's still the initial acquire mode,
        which is intended for ensuring, that a certain executable is
        called only once. (will_own=1)
        In this case the calling process insists to own the mutex and
        fails otherwise.
        In the other contexts the first process will create the mutex.
    """

    def __init__(self, name, will_own=1, lockdir=None):
        self.name = name
        self.will_own = will_own
        if not will_own:
            self.handle = CreateMutex(None, self.will_own, self.name)
        else:
            self.handle = None

    def acquire(self, timeout=TIMEOUT_INFINITE):
        """ gets mutex
            due to legacy reasons there's still the initial acquire mode,
            which is intended for ensuring, that a certain executable is
            called only once. (will_own=1)
        """
        if self.will_own:
            self.handle = CreateMutex(None, self.will_own, self.name)
            err = GetLastError()
            if err == ERROR_ALREADY_EXISTS:
                return False
            else:
                return self
        rslt = WaitForSingleObject(self.handle, timeout)
        if rslt == MTX_WAIT_OBJECT_O:
            return self
        elif rslt == MTX_WAIT_TIMEOUT:
            return False
        raise IPCMutexError("got got return code %08x" % rslt)

    def release(self):
        """ releases a mutex. Raises exception if error """
        # TODO: could fetch enhanced error info with GetLastError()
        rslt = ReleaseMutex(self.handle)
        if rslt == 0:
            raise IPCMutexError("could not release Mutex.")
