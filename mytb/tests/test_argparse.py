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
        self.assertEqual(options.log_config, None)

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
