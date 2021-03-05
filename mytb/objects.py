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

