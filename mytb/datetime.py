from __future__ import absolute_import
from __future__ import print_function

import pytz
import re
import tzlocal

from datetime import datetime
from datetime import timedelta

import dateutil.parser


# datetime objct for beginning of epoch
T_EPOCH = datetime(1970, 1, 1, tzinfo=pytz.utc)
DEFAULT = object()  # singleton, for args with default values


class DateTimeError(Exception):
    """ custom exception """


class DateTime(object):
    single_delta = r'(?:\s*([+-]\d+(?:\.\d*)?)(?:\s*([shMdw])?)\s*)'
    single_delta = r'(?:\s*([+-]\d+(?:\.\d*)?)\s*([shMdw]?)\s*)'
    # attempt to handle comma separated list of deltas
    # multi_delta = r'^%s(?:,%s)*$' % (single_delta, single_delta)
    delta_rex = re.compile('^' + single_delta + '$')

    delta_units = {
        's': (0, 1),
        'M': (0, 60),
        'h': (0, 3600),
        'd': (1, 0),
        'w': (7, 0),
        '': (1, 0),  # default unit = days
        }

    @classmethod
    def strptimedelta(cls, deltastr, info=None, raise_on_error=True):
        """ parses a date time string and returns a datetime timedelta object
             Supported Formats:
                 '+-<num><unit>'
                 where unit =
                     s for seconds
                     h for hours
                     M for minutes
                     d for days
                     w for weeks
                     default = days
        """
        # not implemented so far
        #             and rounding (use by strptime) =
        #                 d for days
        #                 default no rounding

        #     """
        # TODO: think about using dateutil.parser.relativedelta
        rslt = datetime.now(pytz.utc)
        fields = (val.strip() for val in deltastr.split(','))
        delta_rex = cls.delta_rex
        for field in fields:
            match = delta_rex.match(field)
            if not match:
                raise DateTimeError("can't parse %r as delta" % field)
            value, unit = match.groups()
            value = float(value)
            days, seconds = cls.delta_units[unit]
            rslt += timedelta(days * value, seconds * value)

        return rslt

    @classmethod
    def strptime(cls, datestr=None, fmt=None, tzinfo=DEFAULT):
        """ parses a date time string and returns a date time object
            Supported Formats:
                - formats as supported by dateutil.parser
                - None, '', 0, '0' and 'now' -> datetime.now()
                - if fmt is passed same as datetime.strptime

            :param datestr: date string to be passed
            :param fmt: if passedm then use datetime's normal strptime
                        BUT add a time zone info
            :param tzinfo: if no tz info is specified in the string, then
                this param decides which time zone shall be used.
                DEFAULT: use local time zone
                None: return naive time zone object
                other: use other time zone

        """
        #    NOT IMPLEMENTED SO FAR
        #        - delta format with +-num units[rounding],
        #        where unit =
        #            s for seconds
        #            M for minutes
        #            h for hours
        #            d for days
        #            w for weeks
        #        and rounding =
        #            d for days
        #            default no rounding

        tzinfo = tzinfo if tzinfo is not DEFAULT else tzlocal.get_localzone()
        if fmt:
            rslt = datetime.strptime(datestr, fmt)
        else:
            if isinstance(datestr, (int, float)):
                datestr = str(datestr)
            datestr = datestr.strip() if datestr else datestr
            if datestr in (None, '', '0', 'now'):
                return datetime.now(tzinfo)
            if datestr[:1] in "+-" or ',' in datestr:
                return cls.strptimedelta(datestr, tzinfo)

            rslt = dateutil.parser.parse(datestr)

        if rslt.tzinfo is None and tzinfo:
            rslt = tzinfo.localize(rslt)
        return rslt

    @classmethod
    def parse_range(cls, rangestr=None, default_from='-1d', default_to='now'):
        """ parses a time range string
            a time range string is a comma separated list of a start time
            and a end time
        """

        if rangestr is None:
            from_str = default_from
            to_str = default_to
        else:
            from_str, to_str = [v.strip() for v in rangestr.split(',', 1)]
            from_str = from_str if from_str else default_from
            to_str = to_str if to_str else default_to
        t_from = cls.strptime(from_str)
        t_to = cls.strptime(to_str)
        return t_from, t_to


class Time(DateTime):
    @classmethod
    def strptime(cls, datestr):
        pass


class Date(DateTime):
    @classmethod
    def strptime(cls, datestr):
        pass


def fname_to_time(fname, use_ctime=False, use_mtime=False, tz=None):
    """ extracts date time from an fname
        examples of supported formats:
            "fnameYYYYMMDD"            just a date
            "fnameYYYY-MM-DD"          date with separators
            "fnameYYYYMMDD_HHmmss"     date and time
            "fnameYYYYMMDD-HHmmss"     date and time
            "fnameYYYYMMDD-HH-mm-ss"   date and time
            "fnameYYYYMMDD-ssssssssss" date and time(in seconds since epoche)

        :param fname: file name to parse
        :param use_ctime: if file name contains no string use file's ctime
        :param use_mtime: if file name contains no string use file's mtime

    """


def to_timestamp(t):
    """ convert a datetime object to seconds since epoch """
    return (t - T_EPOCH).total_seconds()
