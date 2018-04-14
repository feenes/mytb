#!/usr/bin/env python
# #############################################################################
# Copyright : (C) 2017 by Teledomic.eu All rights reserved
#
# Name:         mytb.commands
#
"""
    Entry point for mytb commands
"""
#
# #############################################################################
from __future__ import print_function

# python std modules
import argparse
import sys

# third party modules
import minibelt

# TODO: add autodiscovery
commands = [(
        "check_ci_cfg", "mytb.gitlab.check_ci_cfg.main",
        "checks config of a gitlab ci cfg",
        )]

cmd_dict = dict((entry[0], entry[1:]) for entry in commands)


def show_commands(options=None):
    """ shows list of available commands """
    print("available mytb commands:")
    for entry in commands:
        cmd, mod, helptext = entry
        print("%18s: %s" % (cmd, helptext))


def mk_parser():
    parser = argparse.ArgumentParser(description="entrypoint for mytb scripts")
    parser.add_argument(
            "cmd", nargs=argparse.REMAINDER,
            help="command to call")
    return parser


def main():
    """ the main function """
    args = sys.argv[1:]
    parser = mk_parser()
    options = parser.parse_args(args)
    cmd = options.cmd
    if not cmd:
        show_commands(options)
        return
    cmd_name = cmd[0]
    if cmd_name not in cmd_dict:
        print("ERROR: command %s is unnown:\n" % cmd_name)
        show_commands(options)
        sys.exit(255)

    mod, _help_text = cmd_dict[cmd_name]
    func = minibelt.import_from_path(mod)
    sys.argv = args
    func()


if __name__ == "__main__":
    main()
