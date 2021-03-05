#!/usr/bin/env python

# ############################################################################
# Copyright  : (C) 2015-2021 by MHComm. All rights reserved
#
# Name       :  mytb.pickle
"""
  Summary    : pickle / unpickle related helpers

__author__    = "Klaus Foerster"
__email__     = "info@mhcomm.fr"


Current implementation is just a dummy for the mhflt tool.

robust pickling / unpickling should be implemented lateron
"""
# #############################################################################
import pickle

from io import BytesIO


def robust_unpickler(fin):
    """
    an unpickler that tries to be more robust.

    At the moment this is just a dummy
    """
    return pickle.Unpickler(fin)


def unpickle_robust(bytestr):
    """ robust unpickle of one byte string """
    fin = BytesIO(bytestr)
    unpickler = robust_unpickler(fin)
    return unpickler.load()
