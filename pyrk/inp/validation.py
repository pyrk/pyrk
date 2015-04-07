from ur import units

def validate_ge(valname, val, llim):
    """Raises errors if the value is less than the lower limit (llim) or if it
    is of the wrong type"""
    if validate_num(valname, val) < llim:
        msg = valname + " must be greater than or equal to "
        msg += str(llim) + ".\n"
        msg += "The value provided was : "
        msg += str(val)
        raise ValueError(msg)

    return val


def validate_le(valname, val, ulim):
    """Raises errors if the value is greater than the upper limit (ulim) or if it
    is of the wrong type"""
    if validate_num(valname, val) > ulim:
        msg = valname + " must be less than or equal to "
        msg += str(ulim) + ".\n"
        msg += "The value provided was : "
        msg += str(val)
        raise ValueError(msg)

    return val


def validate_num(valname, val):
    if isinstance(val, (int, long, float, units.Quantity)):
        return val
    else:
        msg = valname + " must be an integer, long, float, or Quantity.\n"
        msg += "The value provided was of type " + str(type(val))
        msg += " and value "
        msg += str(val)
        raise TypeError(msg)


def validate_not_none(valname, val):
    if val is not None:
        return val
    else:
        msg = valname + " must be instantiated with a non null value.\n"
        msg += "The value provided was None"
        raise TypeError(msg)
