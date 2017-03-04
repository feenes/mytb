#!/usr/bin/env python
from __future__ import absolute_import, print_function

# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.logging.config
#
# Description:  helpers to get fast and quick a decent log configuration
#
# #############################################################################
import os
import sys
import logging
import re
import inspect
import __main__

from mytb.pprint import pprint


def shall_configure_logging(name=None):
    """ tries to determine whether we should configure
        logging or not
    """
    if name == "__main__": # simple case. just cfg logging
        return True

    # let's inspect the call stack
    print("MAIN FILE", __main__.__file__)
    stack = inspect.stack()
    #print(len(stack), "stack entries")
    assert len(stack) >= 3  # at least stack entries should be there
    #pprint(stack, "STACK")
    record = stack[2]
    #pprint(record, "\n\nrecord")
    frm, fname, lno, funcname = record[:4]
    if fname == __main__.__file__:
        print("CALLED BY MAIN")
        return True


def split_config(log_config):
    """ splits log config int the config name and its arguments 
        This is not fully implemented. it will split on ' ' or on ':' depending what occurs first
    """
    splitvals = re.split('(\s+|:)', log_config, 1)
    if len(splitvals) == 2:
        cfg_name, cfg_args = splitvals
    else:
        cfg_name = log_config
        cfg_args = {}
    return cfg_name, cfg_args


def config_logger(cfg_name, name):
    """ tries to locate a log configuration and apply it
        rules:
        1.) split cfg_name into cfg_name and cfg_args
        2.) if cfg_name is a file name, the determine its file type and load it
                accordingly. only python files will handle the passed args
        3.) for cfg_names, that are NOT a file try to import following module in following order
               <cfg_name>
               log_settings.<cfg_name>
               log_settings.<cfg_name>_default
               log_settings.default
               log_settings.default_default
            accept the first module, that contains a dict named LOGGING 
            or has a callable named get_log_settings(), or a callable setup_logging()
    """
    print("CONFL", cfg_name, name, sys.argv[:1])
    if cfg_name is None:
        if name == "__main__":
            name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        cfg_name = name
    
    cfg_name, cfg_args = split_config(cfg_name)
    if os.path.isfile(cfg_name):
        suffix = os.path.splitext(cfg_name).lower()
        #allowed_suffixes = [ '.json', '.yaml', '.ini', '.py', '.pyw', '.pyc', '.pyo' ]
        allowed_suffixes = [ '.py', ]
        if  suffix in allowed_suffixes:
            print("setup logging from file %s" % cfg_name)
            if suffix == ".py" and cfg_args:
                print("cfg args are %r" % cfg_args)
            raise NotImplementedError("still to be coded")
            return
    modnames = (
            "{0} log_settings.{0} log_settings.{0}_default "
            "log_settings.default log_settings.default_default"
            ).format(cfg_name).split()
    
    print(repr(modnames))


def getLogger(name=None, force_config=False):
    print("GETL", name)
    if force_config or shall_configure_logging(name):
        from mytb.argparse import mk_parser, LONG_LOG_SWITCH
        args = sys.argv[1:]
        parser = mk_parser()
        options, unknown = parser.parse_known_args(args)
        print("OPTIONS", options)
        log_cfg = getattr(options, LONG_LOG_SWITCH[2:].replace('-', '_'))
        config_logger(log_cfg, name)
        print("SHALL CONFIG")
    return logging.getLogger(name)
