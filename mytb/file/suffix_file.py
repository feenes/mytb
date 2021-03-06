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


class SuffixFile(object):
    """ Fileobject, that will inspect its suffix to decide how to open
    """
    # TODO: Implement suffixes
    @classmethod
    def open(cls, fname, mode="r", **kwargs):
        """ opens file with respective compression / decompression """
        return open(fname, mode, **kwargs)
