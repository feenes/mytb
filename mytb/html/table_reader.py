#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
# ############################################################################
# Copyright  : (C) 2014 by MHComm. All rights reserved
#
# module released to mytb. under mytb's license
#
# Name       :  mytb.html.table_reader
"""
  Summary    : reads html tables as for example done by xls exports

__author__    = "Klaus Foerster"
"""
# #############################################################################

import logging

from collections import deque
from collections import OrderedDict

from io import open

from six.moves import html_parser
from six import binary_type, text_type


string_types = (binary_type, text_type)
logger = logging.getLogger(__name__)


class TableParser(html_parser.HTMLParser):
    """ simple parser  parsing the first table in an html document """
    S_INIT = 0
    S_TABLE = 1
    S_ROW = 2
    S_COL = 3

    def __init__(self):
        html_parser.HTMLParser.__init__(self)
        self.to_yield = deque()
        self.state = self.S_INIT
        self.tagcnt = 0
        self.rowdata = []
        self.celldata = []
        self.max_cnt = 0

    def handle_starttag(self, tag, attrs):
        state = self.state
        self.tagcnt += 1
        if state == self.S_INIT:
            if tag == 'table':
                self.state = self.S_TABLE
        elif state == self.S_TABLE:
            if tag == 'tr':
                self.state = self.S_ROW
                self.rowdata = []
        elif state == self.S_ROW:
            if tag == 'td':
                self.state = self.S_COL
                self.celldata = []
        elif state == self.S_COL:
            pass

    def handle_data(self, data):
        state = self.state
        if state == self.S_COL:
            self.celldata.append(data)

    def handle_endtag(self, tag):
        state = self.state
        if state == self.S_INIT:
            pass
        elif state == self.S_TABLE:
            if tag == 'table':
                self.state = self.S_INIT
        elif state == self.S_ROW:
            if tag == 'tr':
                self.state = self.S_TABLE
                self.to_yield.append(list(self.rowdata))
        elif state == self.S_COL:
            if tag == 'td':
                self.state = self.S_ROW
                self.rowdata.append(''.join(self.celldata))


class TableReader(object):
    def __init__(self, fin, encoding='utf-8'):
        """
            :param fin: input file or iterator yielding
                    characters from an object
        """
        self._from_fname = False
        if type(fin) in string_types:
            fin = open(fin, encoding=encoding)
            self._from_fname = True

        self.fin = fin
        self.parser = TableParser()
        self.cnt = 0

    def rows(self):
        parser = self.parser
        to_yield = parser.to_yield
        try:
            for line in self.fin:
                self.cnt += 1
                parser.feed(line)

                while len(to_yield):
                    rslt = to_yield.popleft()
                    yield rslt
        except Exception:
            pass
        finally:
            if self._from_fname:
                self.fin.close()

    def __iter__(self):
        return self.rows()


class TableDictReader(TableReader):
    """ Table reader returning dicts
    """
    def rows(self, cls=OrderedDict):
        """
        :param :cls dict class or factory to construct
            an iterated object from header row / data row
        """
        rows = TableReader.rows(self)
        head_row = next(rows)
        logger.debug("HEADROW %r", head_row)
        for row in rows:
            if len(row) != len(head_row):
                row = row + [None] * (len(head_row) - len(row))
            yield cls(zip(head_row, row))


def main():
    pass


if __name__ == '__main__':
    main()
# -----------------------------------------------------------------------------
#   End of file
# -----------------------------------------------------------------------------
