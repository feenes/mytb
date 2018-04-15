from __future__ import absolute_import
from __future__ import print_function


# -----------------------------------------------------------------------------
#   Imports
# -----------------------------------------------------------------------------
import threading
import logging

from builtins import input


logger = logging.getLogger(__name__)


class CLI(object):
    input_func = input

    def __init__(self, options=None, namespace=None, quit_func=None):
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
        try:
            from IPython.terminal.embed import InteractiveShellEmbed
            use_ipython = True
            logger.debug("CLI using ipython")
        except ImportError:
            use_ipython = False
            logger.debug("CLI using basic fallback")

        if use_ipython:
            shell = InteractiveShellEmbed(user_ns=namespace)
            shell()

        else:
            self.mini_shell(namespace=namespace)

        if self._quit_function:
            try:
                self._quit_function(self)
            except TypeError:
                logger.warning("using obsolete quit function without argument")
                self._quit_function()

    def mini_shell(self, namespace):
        """ Rather lousy Python shell for debugging.
            Just in case ipython is not installed or has the wrong version
        """
        while True:
            cmd_line = self.input_func('-->')
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
