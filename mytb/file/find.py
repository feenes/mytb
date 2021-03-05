#!/usr/bin/env python

# ############################################################################
# Copyright  : (C) 2014-2021 by MHComm. All rights reserved
#
# Name       :  mytb.file.find
"""
  Summary    : filefind helpers

__author__    = "Klaus Foerster"
__email__     = "info@mhcomm.fr"

"""
# #############################################################################
import os


# TODO: check if we get this faster / more effient with python3
def file_find_tuple(basedir, relpath=False, dir_filter=None, file_filter=None):
    if relpath is True:
        relpath = basedir
    for bdir, dirs, files in os.walk(basedir):
        if dir_filter:
            dirs[:] = [adir for adir in dirs if dir_filter(adir)]
        dirs[:] = sorted(dirs)
        if relpath:
            bdir = os.path.relpath(bdir, relpath)
        if file_filter:
            files = [fname for fname in files if file_filter(fname)]
        for fname in sorted(files):
            yield (bdir, fname)


def file_find(basedir, relpath=False, dir_filter=None, file_filter=None,
              path_filter=None):
    found_tuples = file_find_tuple(basedir, relpath, dir_filter, file_filter)
    full_paths = (os.path.join(bdir, fname) for bdir, fname in found_tuples)
    if path_filter:
        for full_path in full_paths:
            if path_filter(full_path):
                yield full_path
    else:
        for full_path in full_paths:
            yield full_path
