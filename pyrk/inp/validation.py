import sys

from pyrk.utilities.ur import units

if sys.version_info > (3,):
    long = int


def validate_ge(valname, val, llim):
    """Raises errors if the value is less than the lower limit (llim) or if it
    is of the wrong type

    :param valname: the name of the value being validated
    :type valname: string
    :param val: the value to be validated
    :type val: should be a number (or pint.Quantity)
    :param llim: the lower limit of acceptable value for val
    :type llim: the same type as val
    """

    print(valname, val, llim)
    if validate_num(valname, val) < llim:
        msg = valname + " must be greater than or equal to "
        msg += str(llim) + ".\n"
        msg += "The value provided was : "
        msg += str(val)
        raise ValueError(msg)
    else:
        return val


def validate_g(valname, val, llim):
    """Raises errors if the value is less than the lower limit (llim) or if it
    is of the wrong type

    :param valname: the name of the value being validated
    :type valname: string
    :param val: the value to be validated
    :type val: should be a number (or pint.Quantity)
    :param llim: the lower limit of acceptable value for val
    :type llim: the same type as val
    """
    print(valname, val, llim)
    if not validate_num(valname, val) > llim:
        msg = valname + " must be greater than"
        msg += str(llim) + ".\n"
        msg += "The value provided was : "
        msg += str(val)
        raise ValueError(msg)
    else:
        return val


def validate_le(valname, val, ulim):
    """Raises errors if the value is greater than the upper limit (ulim) or if it
    is of the wrong type

    :param valname: the name of the value being validated
    :type valname: string
    :param val: the value to be validated
    :type val: should be a number (or pint.Quantity)
    :param ulim: the upper limit of acceptable value for val
    :type ulim: the same type as val
    """
    print(valname, val, ulim)
    if validate_num(valname, val) > ulim:
        msg = valname + " must be less than or equal to "
        msg += str(ulim) + ".\n"
        msg += "The value provided was : "
        msg += str(val)
        raise ValueError(msg)
    return val


def validate_num(valname, val):
    """Checks that val is a number

    :param valname: the name of the value being validated
    :type valname: string
    :param val: the value to be validated
    :type val: should be a number (or pint.Quantity)
    """
    if isinstance(val, (int, long, float, units.Quantity)):
        return val
    else:
        try:
            if isinstance(val.magnitude, (int, long, float, units.Quantity)):
                return val
        except AttributeError:
                pass
    msg = valname + " must be an integer, long, float, or Quantity.\n"
    msg += "The value provided was of type " + str(type(val))
    msg += " and value "
    msg += str(val)
    raise TypeError(msg)


def validate_not_none(valname, val):
    """Checks that val is not None

    :param valname: the name of the value being validated
    :type valname: string
    :param val: the value to be validated
    :type val: any
    """
    if val is not None:
        return val
    else:
        msg = valname + " must be instantiated with a non null value.\n"
        msg += "The value provided was None"
        raise TypeError(msg)


def validate_supported(valname, val, supported):
    """Checks that val is not None

    :param valname: the name of the value being validated
    :type valname: string
    :param val: the value to be validated
    :type val: any
    :param supported: a list or tuple of allowed values for val
    :type supported: list, tuple, anything with "in" functionality
    """
    if val in supported:
        return val
    else:
        msg = valname + " must be instantiated with a value in the list:\n"
        msg += str(supported)
        msg += "\nThe value provided was "
        msg += str(val)
        raise ValueError(msg)
