from itertools import count

from mytb.lru_cache import lru_cache

already_called = {}

ctr = count()
ctr2 = count()


def mk_signature(args, kwargs):
    sig = tuple(args), tuple(kwargs.items())
    print("sig(%s, %s) => %s" % (args, kwargs, sig))
    return sig


@lru_cache(maxsize=128)
def tstfunc(*args, **kwargs):
    """ a function, that returns a unique result for every call """
    rslt = mk_signature(args, kwargs), next(ctr)
    print("Func(%s, %s) => %s" % (args, kwargs, rslt))
    return rslt


@lru_cache(maxsize=4)
def tstfunc2(*args, **kwargs):
    """ a function, that returns a unique result for every call """
    rslt = mk_signature(args, kwargs), next(ctr2)
    print("Func(%s, %s) => %s" % (args, kwargs, rslt))
    return rslt


def test_cache():

    params = (
        ((1, ), {}),
        ((2, ), {}),
        ((1, 2, ), {}),
        (('1', ), {}),
        ((), {'a': 'val'}),
        )

    results = set()
    for args, kwargs in params:
        signature = mk_signature(args, kwargs)
        rslt_signature, rslt = tstfunc(*args, **kwargs)
        print("CALL1: ", signature, rslt_signature, rslt)
        assert signature == rslt_signature

        rslt_signature, rslt2 = tstfunc(*args, **kwargs)
        print("CALL2: ", signature, rslt_signature, rslt2)
        assert signature == rslt_signature
        assert rslt == rslt2
        results.add(rslt)

    results = list(results)
    print("RSLTS", results)

    assert len(results) == len(params)


def test_cache_size():
    """ show, that cache expires if and only if too many results
        are cached
    """
    call1_rslts = []
    for val in range(4):
        rslt_signature, rslt = tstfunc2(val)
        call1_rslts.append((rslt_signature, rslt))

    for val, call1_rslt in zip(range(4), call1_rslts):
        rslt_signature2, rslt2 = tstfunc2(val)
        rslt_signature, rslt = call1_rslt
        assert rslt_signature == rslt_signature2
        assert rslt == rslt2

    call1_rslts = []
    for val in range(5):
        rslt_signature, rslt = tstfunc2(val)
        call1_rslts.append((rslt_signature, rslt))

    for val, call1_rslt in zip(range(5), call1_rslts):
        rslt_signature2, rslt2 = tstfunc2(val)
        rslt_signature, rslt = call1_rslt
        assert rslt_signature == rslt_signature2
        assert rslt + 5 == rslt2
