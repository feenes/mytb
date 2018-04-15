# first party modules
import yaml


class Pattern(object):
    def __init__(self, value):
        if type(value) is dict:
            self.value = yaml.dump(value)
            print(repr(self.value))
        else:
            self.value = value


pass_patterns = [
    Pattern(  # valid cache entry
        dict(cache=dict(key="123", paths=[".", "other"]))
    ),
    Pattern(  # valid stages and before entry
        dict(
            stages=["one", "two"],
            before_script=["one", "two"],
            )
        ),
    Pattern({  # rather complete cfg
        'cache': dict(key="1234", paths=[".", "tst"]),
        'stages': ["one", "two"],
        'before_script': ["one", "two"],
        'setup': dict(
            stage="one",
            script=["cmd1", "cmd2"],
            ),
        'test2': dict(
            stage="one",
            script=["cmd1", "cmd2"],
            tags=["tag1"],
            ),
        }),
]

fail_patterns = [
    Pattern(  # invalid yaml syntax
        " val1:\nval2:\n"
        ),
    Pattern(  # cache has unknown keys
        dict(cache=dict(unknownkey=1))
        ),
    Pattern(  # stages must be list
        dict(stages=3)
        ),
    Pattern(  # stages must be list
        dict(stages=dict(name='bad'))
        ),
    Pattern(  # before_script must be list
        dict(before_script=3)
        ),
    # cache.paths must be list
    Pattern(
        dict(cache=dict(paths=3))
        ),
]
