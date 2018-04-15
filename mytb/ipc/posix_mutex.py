#!/usr/bin/env python
# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.ipc.posix_mutex
#
# Description:  mutex for posix OS implemented via a lock file
#
# #############################################################################

import os
import fcntl
from tempfile import tempdir


class IPCMutex(object):
    def __init__(self, name, will_own=None, lockdir=tempdir):
        self.name = name
        self.lockdir = lockdir
        self.lockfile = None

    def acquire(self):
        """ acquires a mutex """
        lockfile_name = os.path.join(self.lockdir, self.name)
        cur_umask = os.umask(0)
        lockfile = open(lockfile_name, 'w')
        os.umask(cur_umask)
        try:
            fcntl.lockf(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.lockfile = lockfile
            return self
        except IOError:
            return False

    # will be automatically release if process ends
    def release(self):
        raise NotImplementedError("cannot release this mutex at the moment")
