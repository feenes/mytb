from __future__ import absolute_import

from datetime import datetime
from datetime import timedelta

import pytz
import tzlocal

import mytb.datetime

from mytb.datetime import DateTime
# from mytb.datetime import Date
# from mytb.datetime import Time
# from mytb.datetime import fname_to_time
from mytb.datetime import to_timestamp


def check_diff(t1, t2, maxdelta=0.01):
    """ checks whether two time values are sufficiently close """
    absdiff = abs((t1 - t2).total_seconds())
    print(absdiff)
    return absdiff < maxdelta


def test_to_timestamp():
    """ we can convert to epoch seconds
    """
    # check that T_EPOCH is correct
    assert to_timestamp(mytb.datetime.T_EPOCH) == 0

    # check that 1970-01-01 00:00:00 UTC is well 0
    t0 = datetime(1970, 1, 1, tzinfo=pytz.utc)
    assert to_timestamp(t0) == 0

    # check that today can be converted back and forth via utc
    mytz = tzlocal.get_localzone()
    now = datetime.now(mytz)
    ts = to_timestamp(now)

    # check that today can be converted back and forth via local
    utcfromtimestamp = datetime.utcfromtimestamp
    back_utc = pytz.utc.localize(utcfromtimestamp(ts))
    assert back_utc == now

    back_local = mytz.localize(datetime.fromtimestamp(ts))
    assert back_local == now

    # works even after year 2038
    y2040 = datetime(2040, 2, 29, 17, 48, 12, tzinfo=mytz)
    ts = to_timestamp(y2040)
    back_utc = pytz.utc.localize(utcfromtimestamp(ts))
    assert back_utc == y2040


def test_datetime_parse():
    """ we can parse our strings """

    # helper vars
    utc = pytz.utc

    # test now parsing
    now = datetime.now(utc)
    for nowval in (None, '', 0, 'now'):
        mynow = DateTime.strptime(nowval)
        delta = (mynow - now).total_seconds()
        assert delta < 0.01

    # test dflt strptime
    adate = DateTime.strptime("2017-01-01", "%Y-%m-%d", tzinfo=None)
    assert adate == datetime(2017, 1, 1)

    # same but with zime zones
    adate = DateTime.strptime("2017-01-01", "%Y-%m-%d", utc)
    assert adate == utc.localize(datetime(2017, 1, 1))


def test_range():
    now = DateTime.strptime('now')
    t_from, t_to = DateTime.parse_range()
    one_day = timedelta(1)
    assert check_diff(t_from, now - one_day)
    assert check_diff(t_to, now)
