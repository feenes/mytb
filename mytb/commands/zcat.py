#!/usr/bin/env python

# ############################################################################
# Copyright  : (C) 2025 by MHComm. All rights reserved
#
# Name       :  mytb.zcat
"""
  Summary    : cats files and uncompresses if necessary

__author__ = "Klaus Foerster"
__email__ = "info@mhcomm.fr"
"""
# #############################################################################
import argparse
import logging


from pathlib import Path

from mytb.file.suffix_file import SuffixFile

logger = logging.getLogger(__name__)


def fconcat(fpaths, mode="r"):
    """
    iterates through filenames and yields all of it's lines
    """
    for path in fpaths:
        path = path if isinstance(path, Path) else Path(path)
        with SuffixFile(path, mode=mode) as fin:
            for line in fin:
                yield line


def mk_parser():
    """ commandline parser """
    description = "uncompresses (if necessary) and concats files"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        'fname', nargs='*',
        help="file names to cat",
    )
    return parser


def main():
    options = mk_parser().parse_args()
    for line in fconcat(options.fname):
        print(line, end="")


if __name__ == '__main__':
    main()
