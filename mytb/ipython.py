from __future__ import absolute_import
from __future__ import print_function

# #############################################################################
# Copyright : (C) 2019 by Teledomic.eu All rights reserved
#
# Name:         mytb.ipython
#
# Description:  helper to create an interactive python shell
#
# Ipython will be used if installed
#
# #############################################################################


try:
    import IPython
    HAVE_IPYTHON = True
except Exception:
    HAVE_IPYTHON = False
    raise


def simple_shell(ctx):
    """ basic interactive shell if ipython is not found
    """
    try:
        import readline  # noqa: F401
    except Exception:
        print("readline not found")
    import code

    shell = code.InteractiveConsole(ctx)
    shell.push("from __future__ import print_function")
    shell.push("from __future__ import absolute_import")
    shell.interact()


def start_shell(ctx=None):
    """ starts an interactive python shell
    """
    ctx = ctx if ctx is not None else {}
    if HAVE_IPYTHON:
        IPython.start_ipython(argv=[], user_ns=ctx)
        return
    else:
        print("ipython not installed")
        simple_shell(ctx)
