#!/usr/bin/env python
from __future__ import absolute_import, print_function

# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.tests.test_argparse
#
# Description:  unit tests for argparser
#
# #############################################################################

import argparse
import unittest


class ArgParseTestCase(unittest.TestCase):
    def test_mkparser(self):
        """ 1 1 2 """
        import mytb.argparse
        parser = mytb.argparse.mk_parser()

        #  find all expected keys in parser
        options = parser.parse_args([])
        self.assertEqual(
            set(vars(options).keys()),
            set(['app_name', 'log_config']))
        self.assertEqual(
            options.log_config,
            'mytb.logging.configs.console:level=WARNING',
            )

        options = parser.parse_args(['-L', ''])
        self.assertEqual(
            options.log_config,
            '',
            )

        #  -L switch works
        options = parser.parse_args(['-L', 'tido'])
        self.assertEqual(options.log_config, 'tido')

        #  --log-config switch works
        options = parser.parse_args(['--log-config', 'todo'])
        self.assertEqual(options.log_config, 'todo')

        #  can override long switch
        mytb.argparse.LONG_LOG_SWITCH = '--lock-cfg'
        parser = mytb.argparse.mk_parser()
        options = parser.parse_args(['--lock-cfg', 'tata'])
        self.assertEqual(options.lock_cfg, 'tata')
        print(options)


def test_add_bool_arg():
    from mytb.argparse import add_bool_argument
    parser = argparse.ArgumentParser()
    add_bool_argument(parser, "-s")
    add_bool_argument(parser, "--long")
    add_bool_argument(parser, "-b", "--boolflag")
    add_bool_argument(
        parser, "-d", "--dataflag",
        help="this is a help text",
        )

    #
    args = ["-s", "--long", "0"]
    options = parser.parse_args(args)
    print("options", options)
    assert options.s is True
    assert options.long is False
    assert options.boolflag is None

    for val in ["1", "true", "yes"]:
        print("options", options)
        args = ["-s", "--long", "0", "-b", val]
        options = parser.parse_args(args)
        assert options.boolflag is True

    for val in ["0", "f", "no"]:
        print("options", val, options)
        args = ["-s", "--long", "0", "-b", val]
        options = parser.parse_args(args)
        assert options.boolflag is False
