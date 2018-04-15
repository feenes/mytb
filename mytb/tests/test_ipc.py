#!/usr/bin/env python
# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.tests.ipc
#
# Description:  ipc test case
#
# #############################################################################
from __future__ import absolute_import
from __future__ import print_function

# import unittest

# from mytb.ipc.mutex import Mutex
#
# class IPCTestCase(unittest.TestCase):
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
