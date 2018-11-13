"""
py2 / py3 compatibility helper for functools.lru_cache
"""
import sys

if sys.version_info >= (3, 2):
    from functools import lru_cache
else:
    from collections import OrderedDict

    UNKNOWN = object()

    def mk_signature(args, kwargs):
        sig = tuple(args), tuple(kwargs.items())
        print("sig(%s, %s) => %s" % (args, kwargs, sig))
        return sig

    def lru_cache(maxsize=128, typed=False):
        """ simple fallback of functools.lru_cache for python2
        """

        cache = OrderedDict()

        def decorate(func):

            def cached_func(*args, **kwargs):

                signature = tuple(args), tuple(kwargs)
                rslt = cache.pop(signature, UNKNOWN)
                if rslt is UNKNOWN:
                    rslt = func(*args, **kwargs)

                cache[signature] = rslt

                if len(cache) > maxsize:
                    key = next(cache.iterkeys())
                    cache.pop(key)

                return rslt

            return cached_func
        return decorate
