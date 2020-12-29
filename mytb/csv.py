#!/usr/bin/env python

import csv


class CSVReader(object):
    def __init__(self, fname, encoding='utf8'):
        self.fname = fname
        self.encoding = encoding
        self.fin = None
        self.rdr = None
        self.itr = iter(self)

    def __enter__(self):

        self.fin = open(self.fname, encoding=self.encoding)
        self.rdr = csv.reader(self.fin)
        return self

    def __exit__(self, typ, value, traceback):
        self.fin.close()

    def __iter__(self):
        for row in self.rdr:
            yield row

    def __next__(self):
        return next(self.itr)
