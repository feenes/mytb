#!/usr/bin/env python
# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.pprint
#
# Description:  lazy pretty print
#
# #############################################################################


def pprint(obj, head=None, indent=1):
    """
    """
    from pprint import PrettyPrinter
    pp = PrettyPrinter(indent=indent)
    if head:
        print(head)
    pp.pprint(obj)
