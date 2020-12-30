#!/usr/bin/env python

# ############################################################################
# Copyright  : (C) 2019 by MHComm. All rights reserved
#
# Name       : mytb.debug
"""
  Summary    :  Helpers for debugging

__email__ = "info@teledomic.eu"
"""
# #############################################################################

import sys
import traceback


def get_debugger_mod():
    """ import and gets a debugger module.
        It will try to import ipbd and if it is not installed the default pdb
    """
    try:
        import ipdb as dbg_mod
    except ImportError:
        import pdb as dbg_mod
    return dbg_mod


def pdb_debug_hook(type_, value, tb):
    """ a debug hook function, that can for example be assigned to
        sys.excepthook in order to start a debugger whenever
        an error occured.

        It also displays a small help text for people who're not
        that used to the python debugger commands.

        This hook will only be activated if run in a terminal
    """

    if not sys.stderr.isatty():  # do not start debugger if no console
        sys.__excepthook__(type_, value, tb)
        return

    dbgr_mod = get_debugger_mod()

    traceback.print_exception(type_, value, tb)
    if dbgr_mod.__name__ == 'pdb':
        print(
            "you can install ipdb to have"
            " a python debugger with slightly better"
            " interactive behaviour (tab-completion)\n")
    print(
        "Press:\n"
        "'w' to get a the stack frame,\n"
        "'u' to move up the stack frame\n"
        "'d' to move down the stack frame\n"
        "'q' to quit\n"
        "'h' for help\n"
        )

    dbgr_mod.pm()
