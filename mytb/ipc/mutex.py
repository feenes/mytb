#!/usr/bin/env python
# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.ipc.mutex
#
# Description:  crossplatform IPC mutex (windows / linux)
#
# #############################################################################
from mytb.os import is_posix, is_windows

if is_posix():
    from .posix_mutex import PosixMutex as IPCMutex
elif is_windows():
    from .win_mutex import WinMutex as IPCMutex
else:
    raise NotImplementedError("mutex for this platform not implemented")

_mutexes = dict()


def Mutex(self, name, lockdir=None):
    """ factory returning an OS specific mutex """
    mutex = _mutexes.get(name) or IPCMutex(name, lockdir=lockdir)
    _mutexes[name] = mutex
    return mutex
