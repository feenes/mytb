#!/usr/bin/env python
from __future__ import absolute_import, print_function

# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.importlib
#
# Description:  helper for locating / importing modules
#
# #############################################################################


def module_exists(modulename):
    """ tries to find out whether a module exists """
    import pkgutil
    moduleparts = modulename.split('.')
    mod = ""
    for part in moduleparts:
        mod += '.' + part if mod else part
        if pkgutil.find_loader(mod) is None:
            return False
    return True


def import_obj(obj_str):
    """ handles input string as module.object
        and imports the module and returns the object
    """
    import importlib
    if ':' in obj_str:
        modname, objname = obj_str.split(':')
    else:
        modname, objname = obj_str.rsplit('.', 1)
    mod = importlib.import_module(modname)
    func = getattr(mod, objname)
    return func
