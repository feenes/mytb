#!/usr/bin/env python
# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.gitlab.check_ci_cfg
#
"""
    validates a gitlab-ci config file rather superficially,
    but still better than no syntax check at all. might be implemented as a
    pre-commit trigger
"""
#
# #############################################################################
from __future__ import absolute_import, print_function

# python std modules
import argparse
import re
import sys

# first party modules
import yaml


rex = re.compile  # compile a regex


def print_nothing(*args, **kwargs):
    pass


trace = print_nothing  # for tracing in verbose mode


class Entry(object):
    def init(self, name_rex, *args, **kwargs):
        self.name = name_rex


def match(key, pattern):
    if hasattr(pattern, 'match'):
        return pattern.match(key)
    else:
        return key == pattern


# attemp of describing a very superficial syntax tree
tree = (
    (
        'cache', (
            ("key",  True),
            ("paths", list),
            ),
        ),
    ('stages', list),
    ('before_script', list),
    (
        rex(r".*"), (
            ('allow_failure', bool),
            ('image', str),
            ('stage', str),
            ('script', list),
            ('tags', list),
            )),
)


def check_cfg(cfg, tree, parent=''):
    """ reursiveley check a cfg struct against a simple syntax tree """
    if type(cfg) is dict:
        for key, value in cfg.items():
            trace("\nKEY", key)
            for tree_entry in tree:
                pattern, subtree = tree_entry
                if match(key, pattern):
                    trace("tree entry", tree_entry)
                    trace("SUBTREE", subtree)
                    treetype = type(subtree)
                    if subtree is True:
                        break
                    elif subtree is str:
                        if type(value) is str:
                            break
                        print("%s.%s must be string" % (parent, key))
                        return False
                    elif subtree is bool:
                        if type(value) is bool:
                            break
                        print("%s.%s must be bool" % (parent, key))
                        return False
                    elif subtree is list:
                        if type(value) is list:
                            break
                        print("%s.%s must be list" % (parent, key))
                        return False
                    elif treetype in (tuple,):
                        if parent:
                            sub_parent = parent + '.' + key
                        else:
                            sub_parent = key
                        result = check_cfg(value, subtree, parent=sub_parent)
                        if not result:
                            return result
                        break
                    else:
                        print("NOT IMPLEMENTED: %s.%s" % (parent, key))
                        return False
            else:
                print("key %s.%s doesn't match" % (parent, key))
                return False
            trace("found")
    return True


def check_cfg_file(fname=None, text=None):
    """ checks whether a gitlabci config file seems to be correct
        The checks are not very extensive, but capture some common
        cases.
    """
    if (sum((1 if val else 0) for val in (fname, text is not None))
            != 1):
        raise Exception("must pass either fname or text")

    if fname:
        with open(fname) as fin:
            text = fin.read()
    try:
        cfg = yaml.load(text)
    except (yaml.parser.ParserError,
            yaml.scanner.ScannerError) as exc:
        print("yaml syntax error")
        print(exc)
        return False

    print("yaml syntax is correct")
    rslt = check_cfg(cfg, tree)
    print("Tree check = ", rslt)
    return rslt


def mk_parser():
    parser = argparse.ArgumentParser(
        description="checks syntax of gitlab ci config file")
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="verbose display",
        )
    parser.add_argument(
        "fname", nargs="?", default='.gitlab-ci.yml',
        help="filename to check (default=%(default)s",
        )
    return parser


def main():
    global trace
    args = sys.argv[1:]
    parser = mk_parser()
    options = parser.parse_args(args)
    if options.verbose:
        trace = print
    fname = options.fname
    ok = check_cfg_file(fname)
    sys.exit(0 if ok else -1)
