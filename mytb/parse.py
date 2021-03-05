#!/usr/bin/env python
# #############################################################################
# Copyright : (C) 2021 by Teledomic.eu All rights reserved
#
# Name:         mytb.parse
#
# Description:  helpers for parsing
#
# #############################################################################
import re

from collections import OrderedDict


def parse_paramstr(argstr, sep=None, sep_re=None):
    """ parse function to parse name1=val2:name2=val2 . . .

        no separator allowed in value strings or keys

        :param argstr: the string to be parsed
        :param sep: if set use to split assigments
        :param sep_re: if set use regex or regex string as separator
        :returns: OrderedDict of keys, values
    """
    assert not(sep and sep_re)  # only one of the params should be set
    if not (sep or sep_re):
        sep = ":"
    if sep:
        assigns = argstr.split(sep)
    else:
        assigns = re.split(sep_re, argstr)

    rslt = OrderedDict()
    for kv in assigns:
        key, val = kv.split('=', 1)
        rslt[key] = val
    return rslt
