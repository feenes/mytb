#!/usr/bin/env python
# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.tests.tst_gitlab
#
# Description:  test cases for mytb.gitlab.check_ci_cfg
#
# #############################################################################
from __future__ import absolute_import, print_function

# python std modules
import os
import unittest

# first party modules
import yaml
from ddt import data, ddt

# mytb modules
from mytb.gitlab.check_ci_cfg import check_cfg_file
from mytb.tempfile import mktemp_fname
from mytb.tests.gitlab.cicfg_patterns import fail_patterns, pass_patterns


@ddt
class GitlabCfg(unittest.TestCase):

    def setUp(self):
        self.tmpfiles = []

    def tearDown(self):
        for fname in self.tmpfiles:
            if os.path.isfile(fname):
                os.unlink(fname)

    def test_can_read_file(self):
        """ can read gitlab-ci-cfg files """
        fname = mktemp_fname()
        self.tmpfiles.append(fname)
        with open(fname, "w") as fout:
            fout.write(yaml.dump(dict(before_script="ls")))

    @data(*pass_patterns)
    def test_pattern_passes(self, pattern):
        """ gitlab-ci-cfg is correct """
        self.assertTrue(check_cfg_file(text=pattern.value))

    @data(*fail_patterns)
    def test_pattern_fails(self, pattern):
        """ gitlab-ci-cfg has errors """
        self.assertFalse(check_cfg_file(text=pattern.value))

#     def test_get_rls_mutex(self):
#         """ can acquire and release a mutex """
#         mutex = Mutex("toto")
#         status = mutex.status
#         print("MST", status)
#         self.assertFalse(mutex.status)
#         mutex.acquire(timeout=1)
#         self.assertTrue(mutex.status)
#         mutex.release()
#         self.assertFalse(mutex.status)
#     def test_ctx_get_rls_mutex(self):
#         """ can acquire and release with context manager """
#         with Mutex("toto", 1) as mutex:
#             pass
#             #self.assertTrue(mutex.status)
#         #self.assertFalse(mutex.status)
#         # can acquire mutex without timeout
#         mutex = Mutex("toto", 1)
#
#
# if __name__ == "__main__":
#     import sys
#     args = sys.argv[1:]
#     if args and args[0] == "test":
#         print("TST")
#         suite = unittest.TestSuite()
#         suite.addTest(IPCTestCase("test_get_rls_mutex"))
#         runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
#         runner.run(suite)
