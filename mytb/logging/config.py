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
import logging.config
import re
import inspect
# import json
import importlib

import __main__

# from mytb.pprint import pprint
from mytb.importlib import module_exists


def get_default_log_settings(**kwargs):
    logdir = kwargs.get('log_dir', '.')
    name = kwargs.get('name', 'mytb')
    enable_file_handler = kwargs.get('logtofile')
    handlers = ["console"]
    cfg = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)-8s %(asctime)s %(process)d"
                          + " %(name)-18s:%(lineno)d %(message)s"
            },
            "simple": {
                "format": "%(levelname)-8s %(asctime)s"
                          + " %(name)-18s:%(lineno)d %(message)s",
                "datefmt": "%H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "level": "WARNING",
                "class": "logging.StreamHandler",
                "formatter": "simple"
            },
        },
        "loggers": {
            "": {
                "level": "INFO",
                "handlers": handlers,
            },
        }
    }
    if enable_file_handler:
        handlers["file"] = {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "%s/%s.log" % (logdir, name),
            "formatter": "verbose"
        }
        handlers = ["file"] + handlers
    # print(cfg['handlers']['file'])
    return cfg


get_log_settings = get_default_log_settings


def shall_configure_logging(name=None):
    """ tries to determine whether we should configure
        logging or not
    """
    if name == "__main__":  # simple case. just cfg logging
        return True

    # let's inspect the call stack
    # print("MAIN FILE", getattr(__main__, '__file__', '?'))
    stack = inspect.stack()
    # print(len(stack), "stack entries")
    assert len(stack) >= 3  # at least stack entries should be there
    #  pprint(stack, "STACK")
    record = stack[2]
    #  pprint(record, "\n\nrecord")
    frm, fname, lno, funcname = record[:4]
    # print("fname", fname)
    if fname == getattr(__main__, '__file__', '?'):
        # print("CALLED BY MAIN")
        return True
    dirname, basename = os.path.split(fname)
    # print("DN", dirname, " BN", basename)
    if (os.path.basename(dirname) == 'commands' and
            os.path.splitext(basename)[0] == '__init__'):
        return False
        # return True


def split_config(log_config):
    """ splits log config int the config name and its arguments
        This is not fully implemented. it will split on ' ' or
            on ':' depending what occurs first
    """
    splitvals = re.split(r'(?:\s+|:)', log_config, 1)
    if len(splitvals) == 2:
        cfg_name, cfg_argstr = splitvals
        cfg_args = {}
        for kv in cfg_argstr.split(','):
            key, val = kv.split('=')
            cfg_args[key] = val
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
        3.) for cfg_names, that are NOT a file try to import following module
            in following order:
               <cfg_name>
               log_settings.<cfg_name>
               log_settings.<cfg_name>_default
               log_settings.default
               log_settings.default_default
            accept the first module, that contains a dict named LOGGING
            or has a callable named get_log_settings(), or a callable
                setup_logging()
    """
    # print("CONFL", cfg_name, name, sys.argv[:1])
    if cfg_name is None:
        if name == "__main__":
            name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        cfg_name = name

    cfg_name, cfg_args = split_config(cfg_name)
    if 'name' not in cfg_args:
        cfg_args['name'] = name
    # print("N: %r / A: %r" % (cfg_name, cfg_args))

    # can I find a config file
    if os.path.isfile(cfg_name):
        suffix = os.path.splitext(cfg_name).lower()
        # allowed_suffixes = [
        #     '.json', '.yaml', '.ini', '.py', '.pyw', '.pyc', '.pyo' ]
        allowed_suffixes = ['.py', ]
        if suffix in allowed_suffixes:
            print("setup logging from file %s" % cfg_name)
            if suffix == ".py" and cfg_args:
                print("cfg args are %r" % cfg_args)
            raise NotImplementedError("config file handling still to be coded")
            return

    modnames = (  # module names to search
            "{0} log_settings.{0} log_settings.{0}_default "
            "log_settings.default log_settings.default_default "
            "mytb.logging.configs.{0} "
            "mytb.logging.config"
            ).format(cfg_name).split()
    for modname in modnames:
        # print("MN", modname)
        try:
            exists = module_exists(modname)
        except ImportError:
            exists = False
        if exists:
            # print(modname, "exists")
            try:
                mod = importlib.import_module(modname)
            except Exception as exc:
                print("Error when import log configuration", exc)
                raise
            # print("MOD:", mod)
            logcfg = getattr(mod, 'LOGGING', None)
            getcfg = getattr(mod, "get_log_settings", None)
            # print("LOGCFG", logcfg)
            # print("GETCFG", getcfg)
            if logcfg:
                log_dict = getattr(mod, 'LOGGING', None)
            elif getcfg:
                # print("GETCFG", getcfg)
                # print("CFGARGS", cfg_args)
                try:
                    log_dict = getcfg(**cfg_args)
                except Exception:
                    print("Error when retrieving log configuration from ",
                          modname)
                    raise
            else:
                log_dict = None
            if log_dict:
                try:
                    logging.config.dictConfig(log_dict)
                except Exception:
                    print("Error when applying log configuration from ",
                          modname)
                    raise
                return
            setupfunc = getattr(mod, "setup_logging", None)
            if setupfunc:
                setupfunc(**cfg_args)
                return


# def mk_default_logger(cfg_name):
#     cfg = json.loads(DEFAULT_DICT_CFG_STR
#                      % dict(cfg_name=cfg_name, logdir='.'))
#     logging.config.dictConfig(cfg)


def getLogger(name=None, force_config=False):
    """ gets a logger (like logging.getLogger()
        and if called from a main module or force_config=True
        setup logging according to some rules
        as described in config_logger()
    """
    # print("GETL %s FC=%s SCL %s" %
    #     (name, force_config, shall_configure_logging(name)))
    if force_config or shall_configure_logging(name):
        from mytb.argparse import mk_parser, LONG_LOG_SWITCH
        args = sys.argv[1:]
        parser = mk_parser(add_help=False)
        options, unknown = parser.parse_known_args(args)
        # print("OPTIONS", options)
        log_cfg = getattr(options, LONG_LOG_SWITCH[2:].replace('-', '_'))
        # print("LOG_CFG: %r" % log_cfg)
        config_logger(log_cfg, name)
    return logging.getLogger(name)
