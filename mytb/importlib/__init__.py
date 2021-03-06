#!/usr/bin/env python
# #############################################################################
# Copyright : (C) 2017-2021 by Teledomic.eu All rights reserved
#
# Name:         mytb.importlib
#
# Description:  helper for locating / importing modules
#
# #############################################################################
import importlib


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
    """
    handles input string as module.object

    and imports the module and returns the object
    """
    if ':' in obj_str:
        modname, objname = obj_str.split(':')
    else:
        modname, objname = obj_str.rsplit('.', 1)
    mod = importlib.import_module(modname)
    return getattr(mod, objname)


def import_if_mod_exists(mod_or_func_str):
    """ attempts to import a module or an object if the
        nodule exists

        returns None if module is not existing and should
        raise an exception if there's another problem
        during the module's import

        :param mod_or_func_str: if str contains ":", then the last
                                part is considered to be an object within
                                the module


    """
    mod_name = mod_or_func_str.split(":")[0]
    get_obj = ":" in mod_or_func_str

    rslt = None
    try:
        if get_obj:
            rslt = import_obj(mod_or_func_str)
        else:
            rslt = importlib.import_module(mod_or_func_str)
    except ModuleNotFoundError as exc:
        msg = str(exc)
        if "'%s'" % mod_name not in msg:
            raise

    return rslt
