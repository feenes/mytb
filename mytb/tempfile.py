#!/usr/bin/env python
# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.tempfile
#
# Description:  helpers for temp files
#
# #############################################################################
# python std modules
import os
import tempfile


def mktemp_fname(suffix='', prefix='tmp', dir=None):
    """ creates a temporary filename and closes all open handles
        in order to be nice with OSes like Windows
    """
    fdesc, fname = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    os.close(fdesc)
    return fname
