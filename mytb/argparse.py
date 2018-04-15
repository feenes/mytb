#!/usr/bin/env python
from __future__ import absolute_import, print_function

# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.argparse
#
# Description:  helper for some common argparser flags
#
# #############################################################################


import os
import sys
import argparse

LONG_LOG_SWITCH = "--log-config"
SHORT_LOG_SWITCH = "-L"
LOG_CONF_ENV_VAR = "MYTB_LOG_CONFIG"


def mk_parser(description="", app_name=None, add_help=True):
    """ creates a parser with some default switches """
    log_config = os.environ.get(LOG_CONF_ENV_VAR)
    # print("LOG_CONFIG = %r" % log_config)

    parser = argparse.ArgumentParser(
        description=description,
        add_help=add_help)
    if not SHORT_LOG_SWITCH:
        parser.add_argument(
            LONG_LOG_SWITCH,
            default=log_config,
            help="name of config module (and params)")
    else:
        parser.add_argument(
            LONG_LOG_SWITCH, '-L',
            default=log_config,
            help=("name of config module (and params) "
                  "default=%(default)s. Can "
                  "be overridden with env var {}".format(LOG_CONF_ENV_VAR))
            )

    if not app_name:
        app_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

    parser.set_defaults(app_name=app_name)

    return parser
