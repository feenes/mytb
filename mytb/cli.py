from __future__ import absolute_import
from __future__ import print_function


# -----------------------------------------------------------------------------
#   Imports
# -----------------------------------------------------------------------------
import threading
import logging

try:
    import IPython.terminal.embed
    HAVE_IPYTHON = True
    HAVE_CODE = False
except Exception:
    HAVE_IPYTHON = False

try:
    import code
    HAVE_CODE = True
except Exception:
    HAVE_CODE = False

from builtins import input


logger = logging.getLogger(__name__)


def simple_code_shell(namespace):
    """ basic interactive shell if ipython is not found
        but code can be imported
    """
    try:
        import readline  # noqa: F401
    except Exception:
        print("readline not found")

    shell = code.InteractiveConsole(namespace)
    shell.push("from __future__ import print_function")
    shell.push("from __future__ import absolute_import")
    shell.interact()


class CLI(object):
    """ cli object
    """

    input_func = input

    def __init__(
            self,
            options=None,
            namespace=None,
            quit_func=None,
            use_code=False,  # use code shell if possible
            use_custom=False,  # use custom shell if possible
            ):

        self.use_ipython = self.use_code = self.use_custom = False
        if HAVE_IPYTHON and not (use_code or use_custom):
            self.use_ipython = True
        elif HAVE_CODE and not use_custom:
            self.use_code = True
        else:
            self.use_custom = True
        self._cli_thread = None
        self._options = options
        if namespace is None:
            namespace = dict(__lock=threading.Lock())
        self.namespace = namespace
        if not hasattr(namespace, '__lock'):
            namespace.update(dict(__lock=threading.Lock()))
        self._lock = namespace['__lock']
        self._quit_function = quit_func

    def set_quit_function(self, func):
        self._quit_function = func

    def run(self):
        """ allows to run an ipython shell with the CLI's context vars """
        namespace = self.namespace

        if self.use_ipython:
            logger.debug("CLI using ipython")
            shell = IPython.terminal.embed.InteractiveShellEmbed(
                user_ns=namespace)
            shell()
        elif self.use_code:
            logger.debug("CLI using basic code fallback")
            simple_code_shell(namespace=namespace)
        else:
            logger.debug("CLI using very basic custom fallback")
            self.mini_shell(namespace=namespace)

        if self._quit_function:
            try:
                self._quit_function(self)
            except TypeError:
                logger.warning("using obsolete quit function without argument")
                self._quit_function()

    def mini_shell(self, namespace):
        """ Rather lousy Python shell for debugging in case code can't be
            imported.
            This is probably only the case for some py2exe / pyinstaller
            versions or other incomplete pythons
        """
        while True:
            try:
                cmd_line = self.input_func('--> ')
            except EOFError:
                cmd_line = "q"

            upper_stripped = cmd_line.strip().upper()
            shall_quit = (upper_stripped == 'Q' or upper_stripped == 'QUIT')
            if shall_quit:
                break
            try:
                eval(compile(cmd_line, '<string>', 'single'), namespace)
            except Exception as exc:
                logger.error('ERROR: %r' % exc)

        print("END OF CLI")
        self.write_history()

    def write_history(self, fname=None):
        pass

    def run_as_thread(self, name='cli', daemon=True):
        """ start cli as a thread
            This is needed for Qt Apps, where the GUI must be called
            in the main thread
        """
        self._cli_thread = cli_thread = threading.Thread(
            target=self.run,
            name=name)
        cli_thread.daemon = daemon
        cli_thread.start()


def main():
    pass


if __name__ == '__main__':
    main()
# -----------------------------------------------------------------------------
#   End of file
# -----------------------------------------------------------------------------
