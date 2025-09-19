#!/usr/bin/env python

# ############################################################################
# Copyright  : (C) 2014-2021 by MHComm. All rights reserved
#
# Name       : mytb.file.suffix_file
"""
  Summary    :  opens files depending on suffix with normal open gzip or bzip

__author__ = "Klaus Foerster"
__email__ = "info@mhcomm.fr"

"""
# #############################################################################

import gzip
import bz2
import sys

from pathlib import Path


class SuffixFile(object):
    """ File like object, that will inspect the filename's suffix to decide
        how to be opened

        filename "-" is handled as stdin
    """

    def __init__(self, fpath, mode="r", **kwargs):
        self.fpath = fpath if isinstance(fpath, Path) else Path(fpath)
        self.mode = "r" if mode is None else mode
        self.file = None
        self.kwargs = kwargs

    def __enter__(self):
        suffix = self.fpath.suffix
        if suffix == ".gz":
            mode = "rt" if self.mode == "r" else self.mode
            self.file = gzip.open(self.fpath, mode, **self.kwargs)
        elif suffix in [".bz", ".bz2"]:
            mode = "rt" if self.mode == "r" else self.mode
            self.file = bz2.open(self.fpath, mode, **self.kwargs)
        elif str(self.fpath) == "-":
            self.file = None
            return sys.stdin
        else:
            self.file = open(self.fpath, self.mode, **self.kwargs)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    @classmethod
    def open(self_or_cls, *fpath, mode=None, **kwargs):
        """ opens file with respective compression / decompression """
        if isinstance(self_or_cls, SuffixFile):
            assert not kwargs and not fpath and not mode
            return self_or_cls.__enter__()
        mode = "r" if mode is None else mode
        return self_or_cls(fpath, mode, **kwargs).__enter__()
