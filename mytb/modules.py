import importlib
import logging
import os
import re


logger = logging.getLogger(__name__)


def get_modules(paths=None, exclude_test=False, report=None):
    """ finds modules in a list of paths """
    suffixes = ['.py', '.pyc', '.pyo']
    if report is None:
        report = {}
        error_modules = report['error_modules'] = []
    for pathdir, mod_prefix in paths:
        for basedir, dirs, files in os.walk(pathdir):
            if exclude_test and 'test' in dirs:  # skip test modules
                dirs.remove('test')
            relpath = os.path.relpath(basedir, pathdir)
            if relpath == '.':
                mod_path = mod_prefix
            else:
                mod_path = mod_prefix + '.' + re.sub(r'[\\/]', '.', relpath)

            # keep only python files
            fnames = (
                fname for fname in files
                if os.path.splitext(fname)[1] in suffixes)

            # get and unify module names
            fnames = set(re.sub(r'\.py[co]?$', '', fname) for fname in fnames)

            # traverse modules in alphabetical order
            for fname in sorted(list(fnames)):
                if fname != "__init__":
                    mod_name = mod_path + '.' + fname
                else:
                    mod_name = mod_path
                try:
                    mod = importlib.import_module(mod_name)
                except Exception:
                    logger.warning("failed importing %r", mod_name)
                    error_modules.append(mod_name)
                yield(mod)


def mk_modname(pm_name):
    """ normalizes a filename or module name
    normalize test name
    examples: "tests/modules/tst_01.py" -> "tests.modules.tst_01"
    examples: "./tests/modules/tst_01.py" -> "tests.modules.tst_01"
    examples: "tests\\modules\\tst_01.py" -> "tests.modules.tst_01"
    """
    mod_name = pm_name
    if os.path.isfile(mod_name):
        mod_name = os.path.splitext(os.path.normpath(pm_name))[0]
        mod_name = mod_name.replace('/', '.')
        mod_name = mod_name.replace('\\', '.')
    return mod_name
