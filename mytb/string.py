def str2bool(val):
    """ converts a string to a boolean value
        if a non string value is passed
        then following types will just be converted to Bool:
            int, float, None

        other types will raise an exception

        inspired by
        https://stackoverflow.com/questions/15008758/
        parsing-boolean-values-with-argparse
    """
    if val is None:
        return None
    if isinstance(val, (bool, int, float)):
        return bool(val)
    if not hasattr(val, "lower"):
        pass
    elif val.lower() in ("yes", "oui", "ja", "true", "t", "y", "1"):
        return True
    elif val.lower() in ("no", "non", "nein", "false", "f", "n", "0", ""):
        return False

    raise ValueError("can't convert %r to bool" % val)
