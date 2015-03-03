

def validate_ge(valname, val, llim):
    """Raises errors if the value is less than the lower limit (llim) or if it
    is of the wrong type"""
    if val < llim:
        msg = valname + " must be greater than or equal to "
        msg += str(llim) + ".\n"
        msg += "The value provided was : "
        msg += str(val)
        raise ValueError(msg)

    return validate_num(valname, val)


def validate_num(valname, val):
    if isinstance(val, int) or isinstance(val, float):
        return val
    else:
        msg = valname + " must be an integer or float.\n"
        msg += "The value provided was of type " + str(type(val))
        raise TypeError(msg)
