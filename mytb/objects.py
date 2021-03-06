import json
import logging

from collections import OrderedDict


logger = logging.getLogger(__name__)


class AnyObj(object):
    """ small object storing arbitrary data in a class
        can be populated via kwargs or via a dict.
        if AnyObj.keys is defined only keys contained in that dict will
        be accepted. others will be ignored
    """

    # TODO: Check whether we shouldn't fail if assigning unknown keys !!!!
    keys = None

    def __init__(self, **kwargs):
        if self.keys is None:
            for akey in kwargs:
                self.__dict__[akey] = kwargs[akey]
        else:
            for akey in kwargs:
                if akey in self.keys:
                    mykey = self.keys.get(akey, akey)
                    self.__dict__[mykey] = kwargs[akey]
        self.convert()

    @staticmethod
    def keys_from_list(key_list):
        return dict((key, key) for key in key_list)

    @classmethod
    def from_dict(cls, a_dict):
        """ populates object from a dict """
        return cls(**a_dict)  # pylint: disable=W0142

    def convert(self):
        """ to be overloaded. permits conversion during object
            creation
        """

    def as_dict(self, recursive=False):
        """ returns vars as a dict """
        adict = vars(self)
        if not recursive:
            return adict
        adict = dict(adict)
        to_update = {}  # don't update a dict while iterating through it
        for key, val in adict.items():
            if hasattr(val, "as_dict"):
                to_update[key] = val.as_dict(recursive=True)
        adict.update(to_update)
        return adict

    def pop(self, attr):
        """ pop / remove an object attribute """
        val = getattr(self, attr)
        delattr(self, attr)
        return val

    def __eq__(self, other):
        return self.as_dict() == other.as_dict()


class VersionObject:
    """ simple wrapper to add type / version info to an object
    """

    o_type = "unknown"
    version = "0.0"

    def __init__(self, data=None, version=None, o_type=None, **hdr_args):
        """ creates a versioned object from data and meta info """
        cls = self.__class__
        if version is None:
            version = cls.version
        self.version = version
        if o_type is None:
            o_type = cls.o_type
        self.o_type = o_type
        self.data = data
        self.hdr_args = OrderedDict(hdr_args.items())

    def as_dict(self):
        """ returns versionobject as dict """
        adict = OrderedDict([("type", self.o_type), ("version", self.version)])
        adict.update(self.hdr_args.items())
        adict["data"] = self.data
        return adict

    @classmethod
    def from_dict(cls, adict):
        """ creates a versioned object from a dict """
        adict = dict(adict)
        o_type = adict.pop("type")
        version = adict.pop("version")
        data = adict.pop("data")
        return cls(data, version, o_type, **adict)

    @classmethod
    def from_json_file(cls, fname):
        logger.debug("FROM_FILE %r", fname)
        with open(fname) as fin:
            data = json.load(fin)
        return cls.from_dict(data)
