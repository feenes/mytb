#!/usr/bin/env python

from __future__ import print_function
from __future__ import absolute_import

import sys
import csv

# 2/3 compatibility w future
from builtins import next
from builtins import object
from builtins import open


IS_PY2 = sys.version_info.major <= 2


class CSVReader(object):
    def __init__(self, fname, encoding='utf8'):
        self.fname = fname
        self.encoding = encoding
        self.fin = None
        self.rdr = None
        self.itr = iter(self)

    def __enter__(self):

        if IS_PY2:
            self.fin = open(self.fname, 'rb')
        else:
            self.fin = open(self.fname, encoding=self.encoding)
        self.rdr = csv.reader(self.fin)
        return self

    def __exit__(self, typ, value, traceback):
        self.fin.close()

    def __iter__(self):
        encoding = self.encoding
        if IS_PY2:
            for row in self.rdr:
                row = [field.decode(encoding)
                       if type(field) == bytes else field
                       for field in row]
                yield row
        else:
            for row in self.rdr:
                yield row

    def __next__(self):
        return next(self.itr)
